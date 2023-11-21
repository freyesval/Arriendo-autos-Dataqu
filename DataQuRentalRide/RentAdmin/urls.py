from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('clientes/', clientes, name='clientes'),
    path('cliente/<int:id>/', getCliente, name='getCliente'),
    path('empresas/', empresas, name='empresas'),
    path('arriendos/', arriendos, name='arriendos'),
    path('clientes_ordenados/', getClientSortByLastName, name='clientes_ordenados'),
    path('clientes_ordenados_gastos/', getClientSortByRentExpenses, name='clientes_ordenados_gastos'),
    path('empresas_lista_clientes/', getCompanyClientsSortByName, name='getCompanyClientsSortByName'),
    path('empresa/<int:id_empresa>/clientes/', getClientsSortByAmount, name='getClientsSortByAmount'),
    path('empresas_ganancias/', getCompaniesSortByProfits, name='getCompaniesSortByProfits'),
    path('getCompaniesWithRentsOver1Week/', getCompaniesWithRentsOver1Week, name='getCompaniesWithRentsOver1Week'),
    path('getClientsWithLessExpense/', getClientsWithLessExpense, name='getClientsWithLessExpense'),
    path('agregar_cliente_arriendo/', newClientRanking, name='agregar_cliente_arriendo'),

    path('empresa/<int:id_empresa>/clientes/<int:id_cliente>/', getClientsSortByAmount, name='getClientsSortByAmount'),
]
