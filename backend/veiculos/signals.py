from veiculos.models import QuantVeiculo, TipoVeiculo, TransVeiculo, CategoriaVeiculo
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_QuantVeiculo(sender, **kwargs):
    if sender.name == 'veiculos':
        QuantVeiculo.objects.get_or_create(quant='1-4')
        QuantVeiculo.objects.get_or_create(quant='5-6')
        QuantVeiculo.objects.get_or_create(quant='Mais de 7')

        TipoVeiculo.objects.get_or_create(tipo='Carro')
        TipoVeiculo.objects.get_or_create(tipo='Moto')

        TransVeiculo.objects.get_or_create(transmissao='Manual')
        TransVeiculo.objects.get_or_create(transmissao='Automática')
        TransVeiculo.objects.get_or_create(transmissao='Autonomous')

        CategoriaVeiculo.objects.get_or_create(categoria='Pequeno')
        CategoriaVeiculo.objects.get_or_create(categoria='Médio')
        CategoriaVeiculo.objects.get_or_create(categoria='Grande')
        CategoriaVeiculo.objects.get_or_create(categoria='Luxo')
        CategoriaVeiculo.objects.get_or_create(categoria='SUV')
