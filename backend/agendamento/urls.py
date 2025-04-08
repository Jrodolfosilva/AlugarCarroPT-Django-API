from django.urls import path
from agendamento.views.main import AgendamentoView

urlpatterns = [
    path('agendamento/', AgendamentoView.as_view()),
]