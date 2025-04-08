from rest_framework import serializers
from veiculos.models import Veiculo


class VeiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'

    def to_representation(self, instance):
        dados = super().to_representation(instance)
        dados['foto'] = instance.foto.url
        return dados

class FiltroVeiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'
