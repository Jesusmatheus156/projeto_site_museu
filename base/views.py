from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, date, timedelta
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _ # <<< ADICIONE ESTA LINHA
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q # Essencial para buscas OR
from django.core.paginator import Paginator
from .models import Noticia, ArtigoPesquisa, HorariosDisponiveis, Agendamento 


# Defina as constantes de preço do museu
PRECO_ESTUDANTES = 10.00
PRECO_GERAL = 15.00


# =========================================================================
# 1. VIEWS DE NAVEGAÇÃO
# =========================================================================

def home(request):
    # Exibir as últimas 3 notícias na home
    ultimas_noticias = Noticia.objects.filter(status='Publicado').order_by('-data_publicacao')[:3]
    return render(request, 'base/home.html', {'ultimas_noticias': ultimas_noticias})

def visitar(request):
    return render(request, 'base/visitar.html')

def museu(request):
    return render(request, 'base/museu.html')

def acervo(request):
    return render(request, 'base/acervo.html')

def noticias_page(request):
    # Filtra apenas notícias publicadas para o usuário
    noticias = Noticia.objects.filter(status='Publicado').order_by('-data_publicacao')
    return render(request, 'base/noticias.html', {'noticias': noticias})

def pesquisa(request):
    # Lista todos os artigos de pesquisa (para a listagem com filtros)
    artigos = ArtigoPesquisa.objects.all()
    return render(request, 'base/pesquisa.html', {'artigos': artigos})

@login_required
def dashboard(request):
    total_noticias = Noticia.objects.count()
    total_artigos = ArtigoPesquisa.objects.count()

    return render(request, "dashboard.html", {
        "total_noticias": total_noticias,
        "total_artigos": total_artigos,
    })


# =========================================================================
# 2. VIEWS DE AGENDAMENTO
# =========================================================================

def agendar_visita(request):
    return render(request, 'base/agendar_visita.html')

# API que retorna os horários
def obter_horarios_do_dia(request, data_selecionada):
    try:
        data_obj = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
        data_minima = date.today() + timedelta(days=3)
        
        if data_obj < data_minima:
            return JsonResponse({'error': 'Agendamentos devem ser feitos com no mínimo 3 dias de antecedência.'}, status=400)
        
        # Faz um select_related para evitar consultas N+1 ao acessar o tipo_visita
        horarios = HorariosDisponiveis.objects.select_related('tipo_visita').filter(
            data=data_obj, grupos_disponiveis__gt=0
        ).order_by('hora_inicio')
        
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
    except Exception:
        return JsonResponse({'error': 'Data inválida ou erro interno.'}, status=400)

def processar_agendamento(request):
    if request.method == 'POST':
        # Dados do POST
        nome = request.POST.get('nome_completo')
        telefone = request.POST.get('telefone')
        horario_id = request.POST.get('horario_id')
        tipo_visita = request.POST.get('tipo_visita', 'geral')
        instituicao = request.POST.get('nome_instituicao', '')

        # Pega e valida as quantidades
        try:
            qtd_geral = int(request.POST.get('quantidade_geral', 0)) 
            qtd_estudantes = int(request.POST.get('quantidade_estudantes', 0))
        except ValueError:
            messages.error(request, "Quantidades de visitantes devem ser números válidos.")
            return redirect('agendar_visita')
        
        total_visitantes = qtd_geral + qtd_estudantes
        
        # Validações essenciais
        if not all([horario_id, nome, telefone]) or total_visitantes <= 0:
            messages.error(request, "Preencha todos os campos e selecione pelo menos 1 visitante.")
            return redirect('agendar_visita')
        
        if tipo_visita == 'institucional' and not instituicao.strip():
            messages.error(request, "Para visitas escolares/institucionais, o Nome da Instituição é obrigatório.")
            return redirect('agendar_visita')

        try:
            # Tenta buscar o horário e verifica disponibilidade
            horario = HorariosDisponiveis.objects.select_related('tipo_visita').get(
                id=horario_id, 
                grupos_disponiveis__gt=0
            )
            
            # Validação da regra de 3 dias de antecedência
            data_minima = date.today() + timedelta(days=3)
            if horario.data < data_minima:
                messages.error(request, "Agendamentos devem ser feitos com no mínimo 3 dias de antecedência.")
                return redirect('agendar_visita')

            # Validação da capacidade máxima
            max_capacidade = horario.tipo_visita.capacidade_maxima_pessoas
            if total_visitantes > max_capacidade: 
                messages.error(request, f"O limite máximo de pessoas para este horário é de {max_capacidade} visitantes (o seu agendamento é para {total_visitantes}).")
                return redirect('agendar_visita')

            # Cálculo e Criação do Objeto Agendamento
            valor_total_calculado = (qtd_geral * PRECO_GERAL) + (qtd_estudantes * PRECO_ESTUDANTES)
            
            # Criação do objeto Agendamento
            Agendamento.objects.create(
                nome_completo=nome,
                telefone=telefone,
                horario=horario,
                quantidade_inteira=qtd_geral, 
                quantidade_meia=qtd_estudantes, 
                quantidade_gratuidade=0, 
                nome_instituicao=instituicao,
                valor_total=valor_total_calculado,
                status='Notificado'
            )

            # Decrementa a disponibilidade
            horario.grupos_disponiveis -= 1
            horario.save()
            
            # Montagem da mensagem do Whatsapp
            titulo_visita = "Agendamento Escolar/Institucional" if tipo_visita == 'institucional' else "Agendamento Público Geral"
            detalhe_instituicao = f"Instituição: {instituicao}%0A" if tipo_visita == 'institucional' and instituicao else ""
            
            mensagem = (
                f"Olá! Meu nome é {nome}.%0A"
                f"Gostaria de confirmar meu {titulo_visita} para visita ao museu.%0A%0A"
                f"Data da visita: {horario.data.strftime('%d/%m/%Y')}%0A"
                f"Horário: {horario.hora_inicio.strftime('%H:%M')} às {horario.hora_fim.strftime('%H:%M')}"
                f"{detalhe_instituicao}" 
                f"Quantidade total de visitantes: {total_visitantes}%0A"
                f"   - Público Geral (R$ {PRECO_GERAL:.2f}): {qtd_geral}%0A"
                f"   - Estudantes (R$ {PRECO_ESTUDANTES:.2f}): {qtd_estudantes}%0A%0A"
                f"Valor estimado a ser pago no local: R$ {valor_total_calculado:.2f}%0A"
                f"Agradecemos o agendamento! Aguarde a nossa confirmação final.%0A"
            )
            
            numero_museu = "5584998498911" 
            link_whatsapp = f"https://wa.me/{numero_museu}?text={mensagem}"

            return redirect(link_whatsapp)

        except HorariosDisponiveis.DoesNotExist:
            messages.error(request, "Desculpe, este horário ficou indisponível ou já foi totalmente reservado.")
            return redirect('agendar_visita')
        except IntegrityError: 
            messages.error(request, "Ocorreu um erro ao salvar seu agendamento. Verifique os dados e tente novamente.")
            return redirect('agendar_visita')
        except Exception as e:
            print(f"ERRO INESPERADO NO AGENDAMENTO: {e}") 
            messages.error(request, 'Ocorreu um erro inesperado. Por favor, tente novamente.')
            return redirect('agendar_visita')

    return redirect('agendar_visita')

def detalhe_noticia(request, slug):
    # Busca o objeto Noticia usando o slug, ou levanta um erro 404 se não for encontrado
    noticia = get_object_or_404(Noticia, slug=slug, status='Publicado')
    
    context = {
        'noticia': noticia,
    }
    
    # Certifique-se de que este template existe: base/detalhe_noticia.html
    return render(request, 'base/detalhe_noticia.html', context) 

def noticias_page(request):
    # 1. Pega todas as notícias publicadas ordenadas pela data mais recente
    noticias_list = Noticia.objects.filter(status='Publicado').order_by('-data_publicacao')
    
    # 2. Configura o Paginator com 6 itens por página (ajuste conforme seu design)
    paginator = Paginator(noticias_list, 6)
    
    # 3. Obtém o número da página da URL (default 1)
    page_number = request.GET.get('page')
    
    # 4. Obtém o objeto Page para a página solicitada
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj, 
    }
    return render(request, 'base/noticias.html', context)


def pesquisa(request):
    # ... busca os artigos ...
    artigos_list = ArtigoPesquisa.objects.all().order_by('-data_publicacao')

    # Ação: Mude o segundo parâmetro para 3
    paginator = Paginator(artigos_list, 6) # 3 artigos por página
    
    # ... restante do código de paginação ...
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj, 
    }
    return render(request, 'base/pesquisa.html', context)


def search_results_page(request):
    """
    Realiza a busca em Notícias, Artigos de Pesquisa e Páginas Estáticas.
    """
    query = request.GET.get('q', '').strip() # Pega o termo de busca 'q' da URL
    
    # 1. Definição do Conteúdo Estático de Páginas (Ajuste/Complete o SNIPPET!)
    # É aqui que definimos o texto pesquisável para as páginas que não estão no banco de dados.
    STATIC_PAGES_DATA = [
        {
            'title': _('O Museu - História e Missão'), 
            'url_name': 'museu', 
            'snippet': _('Nossa história, missão e visão. Conheça a fundadora Luiza Cantofa, a trajetória do povo indígenda, e a importância da preservação cultural. Onde estamos, como chegamos aqui.'),
            'icon': 'fa-book-open',
        },
        {
            'title': _('Acervo - Coleções e Artefatos'), 
            'url_name': 'acervo', 
            'snippet': _('Explore nossa coleção de artefatos, cerâmicas, indumentárias, e documentos históricos. Informações sobre catalogação, doações, pesquisa e exposições no acervo.'),
            'icon': 'fa-folder-open',
        },
        {
            'title': _('Visite-nos e Agendamento'), 
            'url_name': 'visitar', 
            'snippet': _('Informações sobre como agendar sua visita, horários disponíveis, preços (inteira, meia, gratuidade), regras de visitação e contato para agendamentos. Ver calendário.'),
            'icon': 'fa-calendar-days',
        },
        # Adicione mais páginas estáticas importantes aqui...
    ]

    noticia_results = []
    artigo_results = []
    static_results = []
    
    if query:
        # 2. Busca em Modelos Dinâmicos (Notícia e ArtigoPesquisa)
        
        # Filtro de Notícias (Título, Chamada, Conteúdo)
        noticia_filter = Q(titulo__icontains=query) | Q(chamada__icontains=query) | Q(conteudo__icontains=query)
        noticia_results = Noticia.objects.filter(
            Q(status='Publicado') & noticia_filter
        ).order_by('-data_publicacao')
        
        # Filtro de Artigos de Pesquisa (Título, Autor, Resumo)
        artigo_filter = Q(titulo__icontains=query) | Q(autor__icontains=query) | Q(resumo_detalhado__icontains=query)
        artigo_results = ArtigoPesquisa.objects.filter(artigo_filter).order_by('-data_publicacao')
        
        # 3. Busca em Páginas Estáticas
        query_lower = query.lower()
        for page in STATIC_PAGES_DATA:
            # Busca no título traduzível e no snippet
            if query_lower in page['title'].lower() or query_lower in page['snippet'].lower():
                static_results.append(page)

    total_results = len(noticia_results) + len(artigo_results) + len(static_results)

    context = {
        'query': query,
        'noticia_results': noticia_results,
        'artigo_results': artigo_results,
        'static_results': static_results, 
        'total_results': total_results,
    }

    # Renderiza o template de resultados (que extenderá base.html)
    return render(request, 'base/search_results.html', context)