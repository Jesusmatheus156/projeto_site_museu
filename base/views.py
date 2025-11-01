# base/views.py
from django.shortcuts import render
from django.http import JsonResponse
from usuario.models import HorariosDisponiveis
from datetime import datetime, date, timedelta

# Suas outras views (home, museu, etc.)
def home(request):
    return render(request, 'base/home.html')

def visitar(request):
    return render(request, 'base/visitar.html')

def museu(request):
    return render(request, 'base/museu.html')

def acervo(request):
    return render(request, 'base/acervo.html')

def CHCTPLA(request):
    return render(request, 'base/CHCTPLA.html')

# View da página de agendamento
def agendamento_interativo_view(request):
    return render(request, 'base/agendamento_interativo.html')

# API que retorna os horários
def obter_horarios_do_dia(request, data_selecionada):
    try:
        data_obj = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
        data_minima = date.today() + timedelta(days=3)
        
        # --- REGRA DE 3 DIAS DE ANTECEDÊNCIA (BACKEND) ---
        if data_obj < data_minima:
            return JsonResponse({'error': 'Agendamentos devem ser feitos com no mínimo 3 dias de antecedência.'}, status=400)
        
        horarios = HorariosDisponiveis.objects.filter(data=data_obj, grupos_disponiveis__gt=0).order_by('hora_inicio')
        
        lista_horarios = []
        for horario in horarios:
            lista_horarios.append({
                'id': horario.id,
                'titulo': horario.tipo_visita.titulo,
                'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
                'hora_fim': horario.hora_fim.strftime('%H:%M'),
                'vagas': horario.grupos_disponiveis,
                'capacidade': horario.tipo_visita.capacidade_maxima_pessoas
            })
        return JsonResponse(lista_horarios, safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Data inválida'}, status=400)