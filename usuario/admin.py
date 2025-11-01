# usuario/admin.py

from django.contrib import admin
from .models import TiposDeVisita, HorariosDisponiveis, Agendamento

@admin.register(TiposDeVisita)
class TiposDeVisitaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'capacidade_maxima_pessoas', 'preco_grupo_fechado')

@admin.register(HorariosDisponiveis)
class HorariosDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora_inicio', 'tipo_visita', 'grupos_disponiveis')
    list_filter = ('data', 'tipo_visita')
    ordering = ('-data', 'hora_inicio')

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    # AQUI ESTÁ A CORREÇÃO:
    # Trocamos 'quantidade_visitantes' por 'quantidade_total_visitantes', que é a soma dos novos campos.
    # Também organizei um pouco melhor as colunas.
    list_display = ('nome_completo', 'horario', 'status', 'quantidade_total_visitantes', 'data_agendamento')

    list_filter = ('status', 'horario__data')
    search_fields = ('nome_completo', 'email', 'telefone')
    readonly_fields = ('data_agendamento',)