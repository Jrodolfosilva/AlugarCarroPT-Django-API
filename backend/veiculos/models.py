from django.db import models

class QuantVeiculo(models.Model):
    quant = models.CharField(max_length=50)

class TipoVeiculo(models.Model):
    tipo = models.CharField(max_length=10)

class TransVeiculo(models.Model):
    transmissao = models.CharField(max_length=20)

class CategoriaVeiculo(models.Model):
    categoria = models.CharField(max_length=20)

class Veiculo(models.Model):
    veiculo = models.CharField(max_length=50)
    quant = models.ForeignKey(QuantVeiculo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoVeiculo, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    transmissao = models.ForeignKey(TransVeiculo, on_delete=models.CASCADE)
    valor_diaria = models.FloatField()
    categoria = models.ForeignKey(CategoriaVeiculo, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='veiculo/')
    placa = models.CharField(max_length=7, unique=True)
    data_inspecao = models.DateField()
    data_proxima_inspecao = models.DateField()


