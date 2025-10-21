from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json

from usuario.models import Usuario, Agendamento

def base(request):
    return render(request, 'base/home.html')

def visitar(request):
    usuario = None
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            usuario = None

    if request.method == 'POST':
        telefone = request.POST.get('telefone')
        tipo_visitante = request.POST.get('tipo_visitante')
        instituicao = request.POST.get('instituicao', None)
        quantidade = request.POST.get('quantidade_visitantes', 1)
        data = request.POST.get('data')
        horario = request.POST.get('horario')

        if tipo_visitante == 'individual':
            quantidade = 1

        Agendamento.objects.create(
            usuario=usuario,
            telefone=telefone,
            tipo_visitante=tipo_visitante,
            instituicao=instituicao if tipo_visitante == 'instituicao' else None,
            quantidade_visitantes=quantidade,
            data=data,
            horario=horario
        )

        messages.success(request, f"Agendamento realizado com sucesso para {data} às {horario}!")
        return redirect('visitar')

    # Monta o dicionário de horários ocupados para o FullCalendar
    agendamentos = Agendamento.objects.all()
    agendamentos_dict = {}
    for ag in agendamentos:
        str_data = ag.data.strftime('%Y-%m-%d')
        if str_data not in agendamentos_dict:
            agendamentos_dict[str_data] = []
        agendamentos_dict[str_data].append(ag.horario.strftime('%H:%M'))

    agendamentos_json = json.dumps(agendamentos_dict, cls=DjangoJSONEncoder)

    context = {
        'usuario': usuario,
        'agendamentos_json': agendamentos_json
    }
    return render(request, 'base/visitar.html', context)

def museu(request):
    return render(request, 'base/museu.html')

def acervo(request):
    return render(request, 'base/acervo.html')

def CHCTPLA(request):
    return render(request, 'base/CHCTPLA.html')
