from utils.jwt.main import MyTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView, Response
from rest_framework import serializers
from django.http import HttpRequest
from user.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'password', 'username', 'telefone', 'nif']

    def save(self, **kwargs):
        self._validated_data['password'] = make_password(self._validated_data['password'])
        self._validated_data['is_staff'] = False
        self._validated_data['is_superuser'] = False
        self._validated_data['is_active'] = True
        return super().save(**kwargs)


class UserView(APIView):

    def post(self, request: HttpRequest):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        telefone = request.data.get('telefone')
        nif = request.data.get('nif')

        if email is None or password is None or username is None or telefone is None or nif is None:
            return Response({'error': 'Campos obrigatórios não preenchidos'}, status=400)

        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "Usuario cadastrado com exito!"}, status=201)
        else:
            return Response(serializer.errors, status=400)

class LoginView(APIView):

    def post(self, request: HttpRequest):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Campos obrigatórios não preenchidos'}, status=400)

        if not Users.objects.filter(email=email).exists():
            return Response({'error': 'Usuário não encontrado'}, status=404)
        else:
            user = Users.objects.get(email=email)
            if not user.check_password(password):
                return Response({'error': 'Usuario ou senha incorreto!'}, status=401)

        user = Users.objects.get(email=email)
        token = MyTokenObtainPairSerializer()
        token = token.get_token(user)
        return Response({'access': str(token.access_token), 'refresh': str(token)}, status=200)
