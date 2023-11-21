from django import forms
from .models import Cliente, Arriendo, Empresa

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'name']

class ArriendoForm(forms.ModelForm):
    class Meta:
        model = Arriendo
        fields = ['id_cliente', 'id_empresa', 'costo_diario', 'dias']