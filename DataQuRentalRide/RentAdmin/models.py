from django.db import models

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.id}'

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.id}'

class Arriendo(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    costo_diario = models.PositiveIntegerField()
    dias = models.IntegerField()