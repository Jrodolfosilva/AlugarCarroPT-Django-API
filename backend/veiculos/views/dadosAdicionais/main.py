from veiculos.models import CategoriaVeiculo, QuantVeiculo, TipoVeiculo, TransVeiculo
from rest_framework import serializers
from rest_framework.views import APIView, Response
from django.http import HttpRequest


class CategoriaVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaVeiculo
        fields = '__all__'

class QuantVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantVeiculo
        fields = '__all__'

class TipoVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVeiculo
        fields = '__all__'

class TransVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransVeiculo
        fields = '__all__'

class dadosAdicionaisViews(APIView):
    def get(self, request: HttpRequest) -> Response:
        categoriaVeiculo = CategoriaVeiculo.objects.all()
        categoriaSerializer =  CategoriaVeiculoSerializer(categoriaVeiculo, many=True)

        quantVeiculo = QuantVeiculo.objects.all()
        quantVeiculoSerializer = QuantVeiculoSerializer(quantVeiculo, many=True)

        tipoVeiculo = TipoVeiculo.objects.all()
        tipoVeiculoSerializer = TipoVeiculoSerializer(tipoVeiculo, many=True)

        transVe = TransVeiculo.objects.all()
        transVeSerializer = TransVeiculoSerializer(transVe, many=True)

        data = {
            'categoriaVeiculo': categoriaSerializer.data,
            'quantVeiculo': quantVeiculoSerializer.data,
            'tipoVeiculo': tipoVeiculoSerializer.data,
            'transVe': transVeSerializer.data
        }

        return Response(data, status=200)
