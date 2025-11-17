# usuario/management/commands/notificar_whatsapp.py
# VERSÃO ATUALIZADA (ENVIA TODOS OS PENDENTES COM PAUSA)

import requests
import json
import time  # <--- ADICIONADO
from django.core.management.base import BaseCommand
from usuario.models import Agendamento
from django.conf import settings # (Recomendado para as chaves)

class Command(BaseCommand):
    help = 'Verifica TODOS os agendamentos pendentes e envia a notificação via TEMPLATE.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando verificação de TODOS os agendamentos pendentes...'))
        self.verificar_e_notificar_todos()
        self.stdout.write(self.style.SUCCESS('Verificação concluída.'))

    def verificar_e_notificar_todos(self):
        
        # 1. Pegamos TODOS os agendamentos pendentes
        agendamentos_pendentes = Agendamento.objects.filter(status='Pendente').select_related('horario__tipo_visita')
        
        # 2. Verificamos se a lista está vazia
        if not agendamentos_pendentes.exists():
            self.stdout.write('Nenhum agendamento pendente encontrado.')
            return
        
        self.stdout.write(self.style.SUCCESS(f'Encontrados {agendamentos_pendentes.count()} agendamentos pendentes. Processando...'))

        # --- Constantes da API (podem ficar fora do loop) ---
        # (Recomendado: Mova-os para settings.py como sugeri antes)
        ACCESS_TOKEN = 'EAAsHkA50ZCzQBPixCryZCsgSOu0zmfhvpl9XZCRfUkiDViMvOv0QA8S85qwsTmpQMK7DTlXaGQEGsXEeXPeekZCrG2CefvbhDFwLKZCpS6vjELhk1YZA3Tg2J3uv4NGJmoYD90SVE4dPJUWzLSFZAoYd6qCAPz635y9pV8gLyJP8s973J4CCWMKJNmWOZAkquLZBWJgZDZD'
        PHONE_NUMBER_ID = '843059088889699'
        NUMERO_PARA_ENVIO = '558498498911' # Número da Coordenação
        NOME_DO_MODELO = 'notificacao_agendamento' 
        API_URL = f'https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages'
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}
        # ----------------------------------------------------

        
        # 3. Criamos o loop para processar CADA agendamento da lista
        for agendamento in agendamentos_pendentes:
            
            self.stdout.write(f"--- Processando Agendamento ID {agendamento.id} ({agendamento.nome_completo}) ---")

            data_formatada = agendamento.horario.data.strftime('%d/%m/%Y')
            hora_formatada = agendamento.horario.hora_inicio.strftime('%H:%M')
            instituicao = agendamento.nome_instituicao or 'Não informado'

            payload = {
                'messaging_product': 'whatsapp',
                'to': NUMERO_PARA_ENVIO,
                'type': 'template',
                'template': {
                    'name': NOME_DO_MODELO,
                    'language': {
                        'code': 'pt_BR'
                    },
                    'components': [
                        {
                            'type': 'body',
                            'parameters': [
                                {'type': 'text', 'text': agendamento.nome_completo}, 
                                {'type': 'text', 'text': agendamento.telefone}, 
                                {'type': 'text', 'text': agendamento.email}, 
                                {'type': 'text', 'text': instituicao}, 
                                {'type': 'text', 'text': str(agendamento.quantidade_inteira)}, 
                                {'type': 'text', 'text': str(agendamento.quantidade_meia)}, 
                                {'type': 'text', 'text': str(agendamento.quantidade_gratuidade)}, 
                                {'type': 'text', 'text': data_formatada}, 
                                {'type': 'text', 'text': hora_formatada} 
                            ]
                        }
                    ]
                }
            }
            
            enviado_com_sucesso = False
            try:
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
                self.stdout.write(f"Resposta da API: {response.json()}")
                if response.status_code == 200:
                    enviado_com_sucesso = True
                else:
                    self.stdout.write(self.style.ERROR(f'Falha no envio para {agendamento.id}: {response.text}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Exceção no envio para {agendamento.id}: {e}'))

            if enviado_com_sucesso:
                agendamento.status = 'Notificado'
                agendamento.save()
                self.stdout.write(self.style.SUCCESS(f"Agendamento {agendamento.id} atualizado para 'Notificado'."))
                
                # 👇 PAUSA DE 10 SEGUNDOS ADICIONADA AQUI
                self.stdout.write(self.style.WARNING("...Aguardando 10 segundos para evitar spam..."))
                time.sleep(10) # Pausa por 10 segundos

            else:
                 self.stdout.write(self.style.WARNING(f"Status do agendamento {agendamento.id} NÃO foi atualizado (envio falhou)."))