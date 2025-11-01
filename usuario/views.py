# usuario/views.py
from django.shortcuts import redirect
from django.contrib import messages
from .models import HorariosDisponiveis, Agendamento
from datetime import date, timedelta

def processar_agendamento(request):
    if request.method == 'POST':
        # PREÇOS (defina os valores do seu museu aqui)
        PRECO_INTEIRA = 20.00
        PRECO_MEIA = 10.00
        
        # Dados do contato
        nome = request.POST.get('nome_completo')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        
        # Dados do agendamento
        horario_id = request.POST.get('horario_id')
        instituicao = request.POST.get('nome_instituicao', '')

        # Pega os novos campos de quantidade do formulário
        qtd_inteira = int(request.POST.get('quantidade_inteira', 0))
        qtd_meia = int(request.POST.get('quantidade_meia', 0))
        qtd_gratuidade = int(request.POST.get('quantidade_gratuidade', 0))

        if not all([horario_id, nome, email, telefone]):
            messages.error(request, "Todos os campos de contato são obrigatórios.")
            return redirect('agendamento_interativo')

        try:
            horario = HorariosDisponiveis.objects.get(id=horario_id, grupos_disponiveis__gt=0)
            
            # Validação extra de segurança para a regra de 3 dias
            data_minima = date.today() + timedelta(days=3)
            if horario.data < data_minima:
                messages.error(request, "Agendamentos devem ser feitos com no mínimo 3 dias de antecedência.")
                return redirect('agendamento_interativo')

            # Cálculo do valor total
            valor_total_calculado = (qtd_inteira * PRECO_INTEIRA) + (qtd_meia * PRECO_MEIA)
            
            # Criação do objeto Agendamento com os campos corretos
            Agendamento.objects.create(
                nome_completo=nome,
                email=email,
                telefone=telefone,
                horario=horario,
                quantidade_inteira=qtd_inteira,
                quantidade_meia=qtd_meia,
                quantidade_gratuidade=qtd_gratuidade,
                nome_instituicao=instituicao,
                valor_total=valor_total_calculado,
                status='Pendente'
            )

            horario.grupos_disponiveis -= 1
            horario.save()
            
            messages.success(request, 'Seu pedido de agendamento foi enviado com sucesso! A equipe do museu entrará em contato para confirmação.')
            return redirect('agendamento_interativo')

        except HorariosDisponiveis.DoesNotExist:
            messages.error(request, "Desculpe, este horário ficou indisponível.")
            return redirect('agendamento_interativo')
    
    return redirect('agendamento_interativo')