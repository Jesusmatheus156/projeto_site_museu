# usuario/urls.py

from django.urls import path
from . import views

# A única URL necessária neste app agora é a que processa o formulário de agendamento.
# Remova todas as outras rotas (login, cadastro, logout, etc.) que você tinha aqui.
urlpatterns = [
    path('processar-agendamento/', views.processar_agendamento, name='processar_agendamento'),
]