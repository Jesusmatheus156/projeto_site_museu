# usuario/management/commands/notificar_whatsapp.py
# VERSÃO DE TESTE FINAL (ENVIA APENAS UM MODELO)

import requests
import json
from django.core.management.base import BaseCommand
from usuario.models import Agendamento

class Command(BaseCommand):
    help = 'Verifica UM agendamento pendente e envia a notificação via TEMPLATE.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando verificação de notificação única (com Modelo)...'))
        self.verificar_e_notificar_um()
        self.stdout.write(self.style.SUCCESS('Verificação concluída.'))

    def verificar_e_notificar_um(self):
        # Pega apenas o primeiro agendamento pendente que encontrar
        agendamento = Agendamento.objects.filter(status='Pendente').select_related('horario__tipo_visita').first()
        
        if not agendamento:
            self.stdout.write('Nenhum agendamento pendente encontrado.')
            return
        
        self.stdout.write(self.style.SUCCESS(f'Encontrado agendamento pendente ID {agendamento.id}. Processando...'))

        # --- SUAS CREDENCIAIS REAIS ---
        
        # 1. Seu Token Permanente
        ACCESS_TOKEN = 'EAAsHkA50ZCzQBPixCryZCsgSOu0zmfhvpl9XZCRfUkiDViMvOv0QA8S85qwsTmpQMK7DTlXaGQEGsXEeXPeekZCrG2CefvbhDFwLKZCpS6vjELhk1YZA3Tg2J3uv4NGJmoYD90SVE4dPJUWzLSFZAoYd6qCAPz635y9pV8gLyJP8s973J4CCWMKJNmWOZAkquLZBWJgZDZD'
        
        # 2. O ID do seu número comprado
        PHONE_NUMBER_ID = '843059088889699'

        # 3. O seu número pessoal para teste (CORRIGIDO COM O CÓDIGO DO PAÍS '55' -> Brasil)
        NUMERO_PARA_ENVIO = '558498498911' 
        
        # 4. O nome do modelo que foi "ATIVO"
        NOME_DO_MODELO = 'notificacao_agendamento' 
        
        # ------------------------------------------------
        
        API_URL = f'https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages'
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}
        
        data_formatada = agendamento.horario.data.strftime('%d/%m/%Y')
        hora_formatada = agendamento.horario.hora_inicio.strftime('%H:%M')
        instituicao = agendamento.nome_instituicao or 'Não informado'

        # Este é o payload CORRETO, usando "template"
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
                            {'type': 'text', 'text': agendamento.nome_completo}, # {{1}}
                            {'type': 'text', 'text': agendamento.telefone},       # {{2}}
                            {'type': 'text', 'text': agendamento.email},          # {{3}}
                            {'type': 'text', 'text': instituicao},                # {{4}}
                            {'type': 'text', 'text': str(agendamento.quantidade_inteira)},  # {{5}
                            {'type': 'text', 'text': str(agendamento.quantidade_meia)},      # {{6}}
                            {'type': 'text', 'text': str(agendamento.quantidade_gratuidade)}, # {{7}}
                            {'type': 'text', 'text': data_formatada},             # {{8}}
                            {'type': 'text', 'text': hora_formatada}              # {{9}}
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
            self.stdout.write(self.style.SUCCESS(f"Agendamento {agendamento.id} ({agendamento.nome_completo}) processado e status atualizado para 'Notificado'."))