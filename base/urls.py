# base/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),         # Sua view para a página inicial
    path('visitar/', views.visitar, name='visitar'),
    path('museu/', views.museu, name='museu'),
    path('acervo/', views.acervo, name='acervo'),
    path('CHCTPLA/', views.CHCTPLA, name='CHCTPLA'),

    # --- LINHAS FALTANDO ---
    # Adicione estas duas linhas para o sistema de agendamento funcionar:

    # 1. A URL que o usuário acessa para ver a página do calendário
    path('agendar/', views.agendamento_interativo_view, name='agendamento_interativo'),
    
    # 2. A URL que o JavaScript usa para buscar os horários de um dia específico
    path('api/horarios/<str:data_selecionada>/', views.obter_horarios_do_dia, name='api_horarios_do_dia'),
]