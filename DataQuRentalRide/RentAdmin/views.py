from django.shortcuts import render, redirect
from .models import Cliente, Empresa, Arriendo
from .forms import *
from django.db.models import F, Sum
from django.http import Http404
import random
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns
import os
from django.conf import settings

def home(request):
    total_arriendos_mes = Arriendo.objects.all().count()
    cliente_mayor_monto = Cliente.objects.annotate(total=Sum('arriendo__costo_diario')).order_by('-total').first()
    cliente_menor_monto = Cliente.objects.annotate(total=Sum('arriendo__costo_diario')).order_by('total').first()

    
    
    clientes = Cliente.objects.values()
    empresas = Empresa.objects.values()
    arriendos = Arriendo.objects.values()
    
    df_clientes = pd.DataFrame.from_records(clientes)
    df_empresas = pd.DataFrame.from_records(empresas)
    df_arriendos = pd.DataFrame.from_records(arriendos)
    
    # Combina los DataFrames
    df = pd.merge(df_arriendos, df_clientes, left_on='id_cliente_id', right_on='id')
    df = pd.merge(df, df_empresas, left_on='id_empresa_id', right_on='id')
    
    # Calcula el costo total de los arriendos para cada cliente en cada empresa
    df['costo_total'] = df['costo_diario'] * df['dias']
    df_grouped = df.groupby(['name_y', 'name_x'])['costo_total'].sum().reset_index()
    
    plt.figure(figsize=(10,6))
    sns.barplot(x='name_y', y='costo_total', hue='name_x', data=df_grouped)
    plt.title('Costo total de arriendos por cliente y empresa')
    plt.xlabel('Cliente')
    plt.ylabel('Costo total')
    plt.show()
    
    fig = plt.gcf()
    image_path = os.path.join(settings.BASE_DIR, 'RentAdmin', 'static', 'grafico.png')
    fig.savefig(image_path)
    
    print(image_path)
    
    
    # Pasa los indicadores al contexto
    context = {
        'total_arriendos_mes': total_arriendos_mes,
        'cliente_mayor_monto': cliente_mayor_monto.name,
        'cliente_menor_monto': cliente_menor_monto.name,
        'image_path': 'grafico.png'
    }
    
    return render(request, 'maintemplate.html', context)

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes':clientes})

def getCliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        raise Http404("Cliente no existe")
    return render(request, 'cliente.html', {'cliente': cliente})


def getClientSortByLastName(request):
    clientes = Cliente.objects.all()

    # Crea una lista de tuplas con el ID y el apellido de cada cliente
    clientes_list = [{'id': cliente.id, 'name': cliente.name, 'rut': cliente.rut} for cliente in clientes]

    # Ordena la lista por apellido
    clientes_list.sort(key=lambda x: x['name'].split(' ')[-1])

    # Crea una lista solo con los IDs de los clientes
    # ids_ordenados = [cliente[0] for cliente in clientes_list]

    return render(request, 'clientes.html', {'clientes': clientes_list}) # ids_ordenados


def getClientSortByRentExpenses(request):
    # Obtén todos los clientes
    clientes = Cliente.objects.all()

    # Crea una lista de diccionarios con los atributos de cada cliente
    clientes_list = []
    for cliente in clientes:
        # Calcula la suma total de los costos de arriendo para cada cliente
        total_gastado = cliente.arriendo_set.annotate(costo_total=F('costo_diario')*F('dias')).aggregate(Sum('costo_total'))['costo_total__sum']
        if total_gastado is not None:
            clientes_list.append({
                'id': cliente.id,
                'name': cliente.name,
                'rut': cliente.rut,
                'total_gastado': total_gastado,
            })

    # Ordena la lista por total gastado en orden decreciente
    clientes_list.sort(key=lambda x: x['total_gastado'], reverse=True)

    return render(request, 'clientes_gastos.html', {'clientes': clientes_list})


def getCompanyClientsSortByName(request):
    empresas = Empresa.objects.all()
    data = {}
    for empresa in empresas:
        clientes = Cliente.objects.filter(arriendo__id_empresa=empresa).order_by('name')
        data[empresa.name] = [cliente.rut for cliente in clientes]
    return render(request, 'empresas_lista_cliente.html', {'data': data})


def getClientsSortByAmount(request, id_empresa, id_cliente=None):
    arriendos = Arriendo.objects.filter(id_empresa=id_empresa)
    data = {}
    for arriendo in arriendos:
        costo_total = arriendo.costo_diario * arriendo.dias
        if arriendo.id_cliente.rut in data:
            data[arriendo.id_cliente.rut] += costo_total
        else:
            data[arriendo.id_cliente.rut] = costo_total
    data = {rut: total_gastado for rut, total_gastado in data.items() if total_gastado > 40000}
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    # Encuentra el ranking del cliente
    ranking = None
    if id_cliente:
        cliente = Cliente.objects.get(id=id_cliente)
        for i, (rut, _) in enumerate(data.items(), start=1):
            if cliente.rut == rut:
                print(f'Ranking encontrado en {i}')
                ranking = i
                break

    return render(request, 'clientes_gasto_empresa_id.html', {'data': data, 'ranking': ranking})


def getCompaniesSortByProfits(request):
    # Obtén todas las empresas 
    empresas = Empresa.objects.all()

    # Crea un diccionario vacío para almacenar las empresas y su total de ingresos
    data = {}

    for empresa in empresas:
        # Calcula la suma total de los ingresos de arriendo para cada empresa
        total_ingresos = Arriendo.objects.filter(id_empresa=empresa).annotate(ingreso_total=F('costo_diario') * F('dias')).aggregate(Sum('ingreso_total'))['ingreso_total__sum']
        if total_ingresos is not None:
            data[empresa.name] = total_ingresos

    # Ordena el diccionario por total de ingresos en orden creciente
    data = dict(sorted(data.items(), key=lambda item: item[1]))

    return render(request, 'empresas_ganancias.html', {'data': data})


def getCompaniesWithRentsOver1Week(request): 
    empresas = Empresa.objects.all()
    diccionario_empresas = {}
    for empresa in empresas:
        arriendos = Arriendo.objects.filter(id_empresa=empresa.id, dias__gte=7)
        diccionario_empresas[empresa.name] = arriendos.count()
    return render(request, 'CompaniesWithRentsOver1Week.html', {'diccionario_empresas': diccionario_empresas})


def getClientsWithLessExpense(request):
    empresas = Empresa.objects.all()
    diccionario_empresas = {}
    for empresa in empresas:
        arriendo = Arriendo.objects.filter(id_empresa=empresa.id).annotate(ganancia=F('costo_diario')*F('dias')).order_by('ganancia').first()
        if arriendo:
            diccionario_empresas[empresa.name] = arriendo.id_cliente.id
    return render(request, 'ClientsWithLessExpense.html', {'diccionario_empresas': diccionario_empresas})


def newClientRanking(request):
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)
        if form_cliente.is_valid():
            cliente = form_cliente.save()
            clientes = list(Cliente.objects.all())
            cliente_aleatorio = random.choice(clientes)
            
            # Crea un nuevo arriendo
            arriendo = Arriendo()
            arriendo.id_cliente = cliente
            arriendo.id_empresa = Empresa.objects.get(name='AUTOK S.A')
            arriendo.costo_diario = 20000
            arriendo.dias = 30
            arriendo.save()
            return redirect('getClientsSortByAmount', id_empresa=arriendo.id_empresa.id, id_cliente=cliente.id)
    else:
        form_cliente = ClienteForm()
    return render(request, 'formulario_arriendo_cliente.html', {'form_cliente': form_cliente})

def empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'empresas.html', {'empresas':empresas})

def arriendos(request):
    arriendos = Arriendo.objects.all()
    return render(request, 'arriendos.html', {'arriendos':arriendos})