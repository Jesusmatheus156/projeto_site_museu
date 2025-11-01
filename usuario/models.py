# usuario/models.py
from django.db import models

class TiposDeVisita(models.Model):
    titulo = models.CharField(max_length=100, help_text="Ex: Até 40 pessoas - COM EDUCADOR")
    capacidade_maxima_pessoas = models.PositiveIntegerField()
    preco_grupo_fechado = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Tipo de Visita"
        verbose_name_plural = "Tipos de Visita"

    def __str__(self):
        return self.titulo

class HorariosDisponiveis(models.Model):
    tipo_visita = models.ForeignKey(TiposDeVisita, on_delete=models.CASCADE, related_name="horarios")
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    grupos_disponiveis = models.PositiveIntegerField(default=1, help_text="Quantos grupos podem agendar neste mesmo horário.")

    class Meta:
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"{self.tipo_visita.titulo} em {self.data.strftime('%d/%m/%Y')} às {self.hora_inicio.strftime('%H:%M')}"

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Notificado', 'Notificado'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    # CAMPOS DO VISITANTE
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    # DADOS DO AGENDAMENTO
    horario = models.ForeignKey(HorariosDisponiveis, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    
    # CAMPOS DE QUANTIDADE DETALHADOS
    quantidade_inteira = models.PositiveIntegerField(default=0, verbose_name="Visitantes (Inteira)")
    quantidade_meia = models.PositiveIntegerField(default=0, verbose_name="Visitantes (Meia-Entrada)")
    quantidade_gratuidade = models.PositiveIntegerField(default=0, verbose_name="Visitantes (Gratuidade)")
    
    nome_instituicao = models.CharField(max_length=255, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    data_agendamento = models.DateTimeField(auto_now_add=True)

    @property
    def quantidade_total_visitantes(self):
        """ Retorna o número total de visitantes no agendamento. """
        return self.quantidade_inteira + self.quantidade_meia + self.quantidade_gratuidade

    def __str__(self):
        return f"Agendamento de {self.nome_completo} para {self.horario.data}"