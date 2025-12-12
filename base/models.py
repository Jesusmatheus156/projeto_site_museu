# base/models.py
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# =========================================================================
# 1. MODELO NOTICIA
# =========================================================================

class Noticia(models.Model):
    STATUS_CHOICES = [
        ('Rascunho', _('Rascunho')),
        ('Publicado', _('Publicado')),
    ]

    titulo = models.CharField(max_length=255, verbose_name=_("Título da Notícia"))
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text=_("URL amigável (deixe em branco para gerar automaticamente)")) 
    
    # CHAMADA/SUBTÍTULO - COM NULL=TRUE PARA MIGRAÇÃO LIMPA
    chamada = models.TextField(
        max_length=300, 
        verbose_name=_("Chamada/Subtítulo (Impacto)"),
        null=True, 
        blank=True,
        help_text=_("Texto curto (máx. 300 caracteres) que resume a notícia e atrai o leitor. Aparece logo abaixo do título principal.")
    )

    # IMAGEM E CRÉDITO
    capa = models.ImageField(upload_to="noticias/capas/", null=True, blank=True, verbose_name=_("Imagem de Capa"))
    
    # LEGENDA E FONTE - COM NULL=TRUE PARA MIGRAÇÃO LIMPA
    legenda_capa = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name=_("Legenda da Imagem de Capa (Alt Text)"),
        help_text=_("Descrição curta da imagem (importante para SEO e acessibilidade).")
    )
    fonte_capa = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_("Fonte/Crédito da Imagem de Capa")
    )

    conteudo = RichTextField(verbose_name=_("Conteúdo Completo (Texto, Imagens, Formatação)"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Rascunho')

    # AUDITORIA
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='noticias_criadas',
        verbose_name=_("Criado Por")
    )
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de Criação"))
    
    data_modificacao = models.DateTimeField(
        auto_now=True, 
        verbose_name=_("Última Modificação")
    )
    modified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='noticias_modificadas',
        verbose_name=_("Modificado Por")
    )
    
    class Meta:
        verbose_name = _("Notícia")
        verbose_name_plural = _("Notícias")
        ordering = ['-data_publicacao']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
    def get_resumo(self):
        if self.chamada:
            return self.chamada[:100] + '...'
        return strip_tags(self.conteudo)[:100] + '...'


# =========================================================================
# 2. MODELO ARTIGO DE PESQUISA (Usando Link Externo)
# =========================================================================

class ArtigoPesquisa(models.Model):
    
    TIPO_PESQUISA_CHOICES = [
        ('monografia', _('Monografia')),
        ('revista', _('Revista')),
        ('dissertacao', _('Dissertação')),
        ('geral', _('Geral/Outros')),
    ]

    titulo = models.CharField(max_length=150, verbose_name=_("Título do Artigo"))
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text=_("URL amigável (deixe em branco para gerar automaticamente)"))
    autor = models.CharField(max_length=150, verbose_name=_("Autor(es)"))
    ano_publicacao_artigo = models.IntegerField(
        null=True, blank=True, 
        verbose_name=_("Ano de Publicação Original (Ex: 2023)"),
        help_text=_("O ano em que o artigo foi efetivamente publicado.")
    )
    
    tipo_pesquisa = models.CharField(
        max_length=20,
        choices=TIPO_PESQUISA_CHOICES,
        default='geral',
        verbose_name=_("Tipo de Publicação")
    )
    
    link_externo_pesquisa = models.URLField(
        max_length=500,
        verbose_name=_("Link Externo da Pesquisa (URL)"),
        help_text=_("Insira o link completo (ex: https://revista.exemplo.com.br/artigo/xyz)")
    )
    
    resumo_detalhado = RichTextField(verbose_name=_("Resumo e Contexto (com formatação)"))
    data_publicacao = models.DateField(auto_now_add=True, verbose_name=_("Data de Cadastro"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = _("Artigo de Pesquisa")
        verbose_name_plural = _("Artigos de Pesquisa")
        ordering = ['-data_publicacao', 'titulo']

    def __str__(self):
        return f"{self.titulo} ({self.autor})"


# =========================================================================
# 3. MODELOS DE AGENDAMENTO
# =========================================================================

class TiposDeVisita(models.Model):
    titulo = models.CharField(max_length=100, help_text=_("Ex: Até 35 pessoas - COM EDUCADOR"))
    capacidade_maxima_pessoas = models.PositiveIntegerField(default=35) 
    preco_grupo_fechado = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = _("Tipo de Visita")
        verbose_name_plural = _("Tipos de Visita")

    def __str__(self):
        return self.titulo

class HorariosDisponiveis(models.Model):
    tipo_visita = models.ForeignKey(TiposDeVisita, on_delete=models.CASCADE, related_name="horarios")
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    grupos_disponiveis = models.PositiveIntegerField(default=1, help_text=_("Quantos grupos podem agendar neste mesmo horário."))

    class Meta:
        verbose_name = _("Horário Disponível")
        verbose_name_plural = _("Horários Disponíveis")
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"{self.tipo_visita.titulo} em {self.data.strftime('%d/%m/%Y')} às {self.hora_inicio.strftime('%H:%M')}"

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('Pendente', _('Pendente')),
        ('Notificado', _('Notificado')),
        ('Confirmado', _('Confirmado')),
        ('Cancelado', _('Cancelado')),
    ]
    
    # CAMPOS DO VISITANTE
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20) 
    
    # DADOS DO AGENDAMENTO
    horario = models.ForeignKey(HorariosDisponiveis, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Notificado')
    
    # CAMPOS DE QUANTIDADE DETALHADOS
    quantidade_inteira = models.PositiveIntegerField(default=0, verbose_name=_("Visitantes (Inteira)"))
    quantidade_meia = models.PositiveIntegerField(default=0, verbose_name=_("Visitantes (Meia-Entrada)"))
    quantidade_gratuidade = models.PositiveIntegerField(default=0, verbose_name=_("Visitantes (Gratuidade)"))
    
    nome_instituicao = models.CharField(max_length=255, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    data_agendamento = models.DateTimeField(auto_now_add=True)

    @property
    def quantidade_total_visitantes(self):
        """ Retorna o número total de visitantes no agendamento. """
        return self.quantidade_inteira + self.quantidade_meia + self.quantidade_gratuidade

    def __str__(self):
        return f"Agendamento de {self.nome_completo} para {self.horario.data}"