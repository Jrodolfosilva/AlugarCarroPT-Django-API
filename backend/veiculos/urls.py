from veiculos.views.dadosAdicionais.main import dadosAdicionaisViews
from veiculos.views.cadastro_carros.CadCarros import CarrosViews, FiltroCarrosViews, CarroIDViews
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('cadastro/carros/', CarrosViews.as_view()),
    path('carros/filtros/', FiltroCarrosViews.as_view()),
    path('info/dados/list/', dadosAdicionaisViews.as_view()),
    path('carro/<str:idCarro>', CarroIDViews.as_view()),
]
