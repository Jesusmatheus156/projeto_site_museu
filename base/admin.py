# base/admin.py
from django.contrib import admin
# Importa todos os modelos do próprio aplicativo base
from .models import Noticia, ArtigoPesquisa, TiposDeVisita, HorariosDisponiveis, Agendamento

# --- 1. ADMIN DA NOTÍCIA ---
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "status", "data_publicacao", "created_by", "modified_by")
    list_filter = ('status', 'data_publicacao')
    search_fields = ("titulo", "chamada", "conteudo")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = 'data_publicacao'
    
    # Campos que o usuário não pode editar manualmente
    readonly_fields = ('data_publicacao', 'data_modificacao', 'created_by', 'modified_by')

    # Agrupamento dos campos para uma melhor visualização no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('titulo', 'slug', 'status', 'chamada', 'conteudo'),
        }),
        ('Mídia e Créditos', {
            # 'classes': ('collapse',), # Opcional: para esconder este bloco por padrão
            'fields': ('capa', 'legenda_capa', 'fonte_capa'),
        }),
        ('Informações de Auditoria', {
            'fields': ('created_by', 'data_publicacao', 'modified_by', 'data_modificacao'),
        })
    )
    
    # MÉTODO CRÍTICO PARA ATRIBUIR O USUÁRIO LOGADO AUTOMATICAMENTE
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Se for um novo objeto (primeira criação)
            obj.created_by = request.user
        
        # Seta o usuário que modificou (sempre na hora de salvar)
        obj.modified_by = request.user
        
        super().save_model(request, obj, form, change)

# --- 2. ADMIN DO ARTIGO DE PESQUISA ---
@admin.register(ArtigoPesquisa)
class ArtigoPesquisaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_pesquisa", "autor", "data_publicacao")
    search_fields = ("titulo", "autor", "resumo_detalhado")
    prepopulated_fields = {"slug": ("titulo",)}
    list_filter = ('tipo_pesquisa', 'ano_publicacao_artigo', 'data_publicacao')
    
    fieldsets = (
        (None, {
            'fields': ('titulo', 'ano_publicacao_artigo', 'tipo_pesquisa', 'autor', 'link_externo_pesquisa', 'resumo_detalhado'),
        }),
        ('Configurações Avançadas', {
            'fields': ('slug',),
            'classes': ('collapse',),
        }),
    )


# --- 3. ADMIN DE AGENDAMENTO ---
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'horario_formatado', 'status', 'quantidade_total_visitantes', 'nome_instituicao', 'data_agendamento')
    list_filter = ('status', 'horario__data', 'nome_instituicao')
    search_fields = ('nome_completo', 'telefone', 'nome_instituicao')
    readonly_fields = ('data_agendamento', 'valor_total')
    ordering = ('-horario__data', 'horario__hora_inicio')

    def horario_formatado(self, obj):
        return f"{obj.horario.data.strftime('%d/%m/%Y')} - {obj.horario.hora_inicio.strftime('%H:%M')}"
    horario_formatado.short_description = "Data/Hora da Visita"
    
    def quantidade_total_visitantes(self, obj):
        # Utiliza o @property do modelo Agendamento
        return obj.quantidade_total_visitantes
    quantidade_total_visitantes.short_description = "Total Visitantes"


# --- 4. ADMIN DE HORÁRIOS E TIPOS ---
@admin.register(TiposDeVisita)
class TiposDeVisitaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'capacidade_maxima_pessoas', 'preco_grupo_fechado')
    search_fields = ('titulo',)

@admin.register(HorariosDisponiveis)
class HorariosDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora_inicio', 'hora_fim', 'tipo_visita', 'grupos_disponiveis')
    list_filter = ('tipo_visita', 'data')
    date_hierarchy = 'data'
    list_editable = ('grupos_disponiveis',)
    ordering = ('data', 'hora_inicio')