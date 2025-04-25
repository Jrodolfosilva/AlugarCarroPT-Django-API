from veiculos.serializers.veiculos import VeiculosSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.jwt.main import MyTokenObtainPairSerializer
from rest_framework.views import APIView, Response
from rest_framework.request import HttpRequest
from veiculos.models import Veiculo, CategoriaVeiculo, QuantVeiculo, TipoVeiculo, TransVeiculo
from agendamento.models import Agendamento
from datetime import datetime, timedelta
from django.db.models import Q

class CarrosViews(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request: HttpRequest) -> Response:
        return Response(VeiculosSerializer(Veiculo.objects.all(), many=True).data, status=200)

    def post(self, request: HttpRequest) -> Response:
        try:
            token = request.headers.get('Authorization').split(' ')[1]
        except:
            return Response({'error': 'Token is required'}, status=401)
        
        user_id = MyTokenObtainPairSerializer.get_id(self, token)
        if user_id != 1:
            return Response({'error': 'You are not authorized to perform this action'}, status=401)

        if request.data.get('foto') == '' or request.data.get('foto') == None:
            return Response({'error': 'image is required'}, status=400)

        if request.data.get('data_inspecao') == '' or request.data.get('data_inspecao') == None:
            return Response({'error': 'data_inspecao is required'}, status=400)

        data_converter =  datetime.strptime(request.data['data_inspecao'], "%d/%m/%Y")

        newData = {
            'veiculo': request.data['veiculo'],
            'quant': request.data['quant'],
            'tipo': request.data['tipo'],
            'marca': request.data['marca'],
            'transmissao': request.data['transmissao'],
            'valor_diaria': request.data['valor_diaria'],
            'categoria': request.data['categoria'],
            'foto': request.data['foto'],
            'placa': request.data['placa'],
            'data_inspecao': datetime.strptime(data_converter.strftime('%Y-%m-%d'), '%Y-%m-%d').date(),
            'data_proxima_inspecao': datetime.strptime((data_converter + timedelta(days=365)).strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        }

        serializer = VeiculosSerializer(data=newData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request: HttpRequest) -> Response:
        try:
            token = request.headers.get('Authorization').split(' ')[1]
        except:
            return Response({'error': 'Token is required'}, status=401)
        
        user_id = MyTokenObtainPairSerializer.get_id(self, token)
        if user_id != 1:
            return Response({'error': 'You are not authorized to perform this action'}, status=401)

        if not 'id' in request.data:
            return Response({'error': 'id is required'}, status=400)

        # Buscando o veículo
        try:
            veiculo = Veiculo.objects.get(id=request.data['id'])
        except Veiculo.DoesNotExist:
            return Response({'error': 'Veiculo not found'}, status=404)

        # Se não houver uma nova foto, mantemos a foto atual
    #    if 'foto' not in request.data or request.data['foto'] is None:
    #        # Adiciona a foto atual do veículo nos dados para o serializer
    #        request.data['foto'] = veiculo.foto 

        if CategoriaVeiculo.objects.filter(id=request.data['categoria']).exists():
            instCategoria = CategoriaVeiculo.objects.get(id=request.data['categoria'])
        else:
            return Response({'error': 'Categoria not found'}, status=404)

        if QuantVeiculo.objects.filter(id=request.data['quant']).exists():
            instQuant = QuantVeiculo.objects.get(id=request.data['quant'])
        else:
            return Response({'error': 'Quant not found'}, status=404)

        if TipoVeiculo.objects.filter(id=request.data['tipo']).exists():
            instTipo = TipoVeiculo.objects.get(id=request.data['tipo'])
        else:
            return Response({'error': 'Tipo not found'}, status=404)

        if TransVeiculo.objects.filter(id=request.data['transmissao']).exists():
            instTrans = TransVeiculo.objects.get(id=request.data['transmissao'])
        else:
            return Response({'error': 'Transmissao not found'}, status=404)

        if request.data.get("foto") == '':
            veiculo_my = Veiculo.objects.get(id=request.data['id'])
            veiculo_my.categoria = instCategoria
            veiculo_my.veiculo = request.data.get('veiculo')
            veiculo_my.quant = instQuant
            veiculo_my.tipo = instTipo
            veiculo_my.marca = request.data.get('marca')
            veiculo_my.transmissao = instTrans
            veiculo_my.valor_diaria = request.data.get('valor_diaria')
            veiculo_my.placa = request.data.get('placa')
            veiculo_my.data_inspecao = request.data.get('data_inspecao')
            veiculo_my.save()
            return Response({'message': 'Veiculo updated successfully'}, status=200)
        else:
            veiculo_my = Veiculo.objects.get(id=request.data['id'])
            veiculo_my.categoria = instCategoria
            veiculo_my.veiculo = request.data.get('veiculo')
            veiculo_my.quant = instQuant
            veiculo_my.tipo = instTipo
            veiculo_my.marca = request.data.get('marca')
            veiculo_my.transmissao = instTrans
            veiculo_my.valor_diaria = request.data.get('valor_diaria')
            veiculo_my.placa = request.data.get('placa')
            veiculo_my.data_inspecao = request.data.get('data_inspecao')
            veiculo_my.foto = request.data.get('foto')
            veiculo_my.save()
            return Response({'message': 'Veiculo updated successfully'}, status=200)


    def delete(self, request: HttpRequest) -> Response:
        try:
            token = request.headers.get('Authorization').split(' ')[1]
        except:
            return Response({'error': 'Token is required'}, status=401)
        
        user_id = MyTokenObtainPairSerializer.get_id(self, token)
        if user_id != 1:
            return Response({'error': 'You are not authorized to perform this action'}, status=401)

        if not 'id' in request.data:
            return Response({'error': 'id is required'}, status=400)

        if not Veiculo.objects.filter(id=request.data['id']).exists():
            return Response({'error': 'Veiculo not found'}, status=404)
        
        veiculo = Veiculo.objects.get(id=request.data['id'])
        veiculo.foto.delete()
        veiculo.delete()
        return Response({'message': 'Veiculo deleted'}, status=200)


class FiltroCarrosViews(APIView):

    def post(self, request: HttpRequest) -> Response:
        dataRequest = {key: value[0] if isinstance(value, list) else value for key, value in request.data.items()}
        data_init = datetime.strftime(datetime.strptime(dataRequest.get('data_init'), "%d/%m/%Y"), "%Y-%m-%d")
        data_end = datetime.strftime(datetime.strptime(dataRequest.get('data_fim'), "%d/%m/%Y"), "%Y-%m-%d")
        dataRequest.pop('data_init')
        dataRequest.pop('data_fim')

        if dataRequest.get('quant') == 'null' or dataRequest.get('quant') == 'undefined' or dataRequest.get('quant') == '':
            dataRequest.pop('quant')

        if dataRequest.get('tipo') == 'null' or dataRequest.get('tipo') == 'undefined' or dataRequest.get('tipo') == '':
            dataRequest.pop('tipo')

        if dataRequest.get('marca') == 'null' or dataRequest.get('marca') == 'undefined' or dataRequest.get('marca') == '':
            dataRequest.pop('marca')

        if dataRequest.get('transmissao') == 'null' or dataRequest.get('transmissao') == 'undefined' or dataRequest.get('transmissao') == '':
            dataRequest.pop('transmissao')

        if dataRequest.get('categoria') == 'null' or dataRequest.get('categoria') == 'undefined' or dataRequest.get('categoria') == '':
            dataRequest.pop('categoria')

        if dataRequest.get('valor_diaria') == 'null' or dataRequest.get('valor_diaria') == 'undefined' or dataRequest.get('valor_diaria') == '':
            dataRequest.pop('valor_diaria')

        if data_init == 'null' or data_init == 'undefined' or data_init == '' or  data_init is None:
            return Response({'error': 'data_init is required'}, status=400)

        if data_end == 'null' or data_end == 'undefined' or data_end == '' or data_end is None:
            return Response({'error': 'data_fim is required'}, status=400)

        veiculos = Veiculo.objects.filter(**dataRequest)

        dataVeiculos = []
        for veiculo in veiculos:
            agendamentos = Agendamento.objects.filter(veiculo=veiculo).filter(
                Q(data_inicio__lte=data_end) & Q(data_fim__gte=data_init)
            ).exists()
            if not agendamentos:
                dataVeiculos.append({
                    'id': veiculo.id,
                    'veiculo': veiculo.veiculo,
                    'quant': veiculo.quant.quant,
                    'tipo': veiculo.tipo.tipo,
                    'marca': veiculo.marca,
                    'transmissao': veiculo.transmissao.transmissao,
                    'valor_diaria': veiculo.valor_diaria,
                    'categoria': veiculo.categoria.categoria,
                    'foto': veiculo.foto.url,
                    'placa': veiculo.placa,
                    'data_inspecao': datetime.strftime(veiculo.data_inspecao, "%d/%m/%Y"),
                })

        return Response(dataVeiculos, status=200)
    


class CarroIDViews(APIView):    


    
    def get (self, request: HttpRequest, idCarro: str) -> Response:
        try:
           
           carro =  Veiculo.objects.filter(id=idCarro).first()

            
        
           newData = {
               'id': carro.id,
               'veiculo': carro.veiculo,
               'quant': carro.quant.quant,
               'tipo': carro.tipo.tipo,
               'marca': carro.marca,
               'transmissao': carro.transmissao.transmissao,
               'valor_diaria': carro.valor_diaria,
               'categoria': carro.categoria.categoria,
               'foto': carro.foto.url,
               'placa': carro.placa,
               'data_inspecao': datetime.strftime(carro.data_inspecao, "%d/%m/%Y"),
           }
        
           return Response(newData,status=200)
        
        except :
            return Response({'error': 'Veiculo not found'}, status=404)


class AllCarros(APIView):
        
        def get(self, request: HttpRequest) -> Response:
            veiculos = Veiculo.objects.all()
            dataVeiculos = []
            for veiculo in veiculos:
                dataVeiculos.append({
                        'id': veiculo.id,
                        'veiculo': veiculo.veiculo,
                        'quant': veiculo.quant.quant,
                        'tipo': veiculo.tipo.tipo,
                        'marca': veiculo.marca,
                        'transmissao': veiculo.transmissao.transmissao,
                        'valor_diaria': veiculo.valor_diaria,
                        'categoria': veiculo.categoria.categoria,
                        'foto': veiculo.foto.url,
                        'placa': veiculo.placa,
                        'data_inspecao': datetime.strftime(veiculo.data_inspecao, "%d/%m/%Y"),
                })


            
            return Response(dataVeiculos, status=200)
        