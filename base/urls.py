# base/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rotas de Navegação
    path('', views.home, name='home_page'),
    path('visitar/', views.visitar, name='visitar'),
    path('museu/', views.museu, name='museu'),
    path('acervo/', views.acervo, name='acervo'),
    path('noticias/', views.noticias_page, name='noticias'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('agendar_visita/', views.agendar_visita, name='agendar_visita'),
    path('api/horarios/<str:data_selecionada>/', views.obter_horarios_do_dia, name='api_horarios_do_dia'),
    path('processar-agendamento/', views.processar_agendamento, name='processar_agendamento'),
    path('noticias/<slug:slug>/', views.detalhe_noticia, name='detalhe_noticia'),
    # Rota Administrativa
    path('dashboard/', views.dashboard, name='dashboard'),
    path('buscar/', views.search_results_page, name='search_results_page'),
]