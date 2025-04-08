from django.db import models


class Agendamento(models.Model):
    userId = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    veiculo = models.ForeignKey('veiculos.Veiculo', on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=100, default='Alugado')
