from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from utils.jwt.main import MyTokenObtainPairSerializer
from rest_framework.views import APIView, Response
from django.http.request import HttpRequest
from agendamento.models import Agendamento
from veiculos.models import Veiculo
from django.db.models import Q
from user.models import Users
from datetime import datetime


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'

# View para lidar com agendamentos
class AgendamentoView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request: HttpRequest):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            user_id = MyTokenObtainPairSerializer().get_id(token)
        except:
            return Response({'error': 'Dados incorreto!'}, status=400)
        user = Users.objects.get(id=user_id)
        dataDados = Agendamento.objects.filter(userId=user)

        new_data = [{
            "userId": data.userId.id,
            "userId_nome": data.userId.username,
            "veiculo": data.veiculo.id,
            "veiculo_nome": data.veiculo.veiculo,
            "veiculo_marca": data.veiculo.marca,
            "data_inicio": data.data_inicio.strftime('%d/%m/%Y'),
            "data_fim": data.data_fim.strftime('%d/%m/%Y'),
            "status": data.status,
            "id": data.id
        } for data in dataDados]

        return Response(new_data, status=200)

    def post(self, request: HttpRequest):
        # Obtendo dados do corpo da requisição
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        telefone = request.data.get('telefone')
        nif = request.data.get('nif')
        veiculo = request.data.get('veiculo')
        data_inicio = datetime.strptime(request.data.get('data_inicio'), '%d/%m/%Y')
        data_fim = datetime.strptime(request.data.get('data_fim'), '%d/%m/%Y')

        if email is None or password is None or veiculo is None or data_inicio is None or data_fim is None:
            return Response({'error': 'Dados incorreto!'}, status=400)

        if not Users.objects.filter(email=email).exists():
            instancia_user = Users.objects.create(
                email=email,
                password=make_password(password),
                username=username,
                telefone=telefone,
                nif=nif
            )
        else:
            instancia_user = Users.objects.get(email=email)

        if not Veiculo.objects.filter(id=veiculo).exists():
            return Response({'error': 'Veiculo não existe!'}, status=400)

        veiculo = Veiculo.objects.get(id=veiculo)

        if (Veiculo.objects.filter(id=veiculo.id).first().data_proxima_inspecao - data_inicio.date()).days < 0:
            return Response({'error': 'Veiculo indisponivel!'}, status=400)

        agendamento = Agendamento.objects.filter(veiculo=veiculo).filter(
            Q(data_inicio__lte=data_fim) & Q(data_fim__gte=data_inicio)
        ).exists()

        if agendamento:
            return Response({'error': 'Veiculo já está agendado!'}, status=400)
        else:
            agendamento_instancia = Agendamento.objects.create(
                userId=instancia_user,
                veiculo=veiculo,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            agendamento_instancia.save()

        return Response({'status' : 'agendamento realizado', 'cod_age' : agendamento_instancia.pk}, status=200)

    def put(self, request: HttpRequest):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            user_id = MyTokenObtainPairSerializer().get_id(token)
        except:
            return Response({'error': 'Dados incorreto!'}, status=400)

        intancia_user = Users.objects.get(id=user_id)

        if not Agendamento.objects.filter(userId=intancia_user, id=request.data.get('id')).exists():
            return Response({'error': 'Agendamento não existe!'}, status=400)

        if request.data.get('data_inicio') is None or request.data.get('data_fim') is None:
            return Response({'error': 'Dados incorreto!'}, status=400)

        date_inicio = datetime.strptime(request.data.get('data_inicio'), '%d/%m/%Y')
        date_fim = datetime.strptime(request.data.get('data_fim'), '%d/%m/%Y')
        date_inicio = datetime.strftime(date_inicio, '%Y-%m-%d')
        date_fim = datetime.strftime(date_fim, '%Y-%m-%d')

        veiculo = Agendamento.objects.filter(id=request.data.get('id')).first().veiculo
        veiculo_id = Agendamento.objects.filter(id=request.data.get('id')).first().veiculo.id

        if (Veiculo.objects.filter(id=veiculo_id).first().data_proxima_inspecao - datetime.strptime(date_inicio, '%Y-%m-%d').date()).days < 0:
            return Response({'error': 'Veiculo indisponivel!'}, status=400)

        agendamento = Agendamento.objects.filter(veiculo=veiculo).filter(
            Q(data_inicio__lte=date_fim) & Q(data_fim__gte=date_inicio)
        ).exists()

        if agendamento:
            return Response({'error': 'Já existe agendamento para essa data!'}, status=400)

        Agendamento.objects.filter(id=request.data.get('id')).update(
            data_inicio=date_inicio,
            data_fim=date_fim
        )

        return Response({'status' : 'Agendamento Autorizado!'}, status=200)

    def delete(self, request: HttpRequest):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            user_id = MyTokenObtainPairSerializer().get_id(token)
        except:
            return Response({'error': 'Dados incorreto!'}, status=400)
        
        user = Users.objects.get(id=user_id)

        if not Agendamento.objects.filter(id=request.data.get('id'), userId=user).exists():
            return Response({'error': 'Agendamento não existe!'}, status=400)

        Agendamento.objects.get(id=request.data.get('id'), userId=user).delete()

        return Response({'status' : 'Cancelamento realizado!'}, status=200)

