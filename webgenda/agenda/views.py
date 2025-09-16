from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import *
from .models import *
import calendar
from datetime import date, datetime, timedelta
import locale
import sys
import json
from dateutil.relativedelta import relativedelta
from operator import itemgetter

MESES_PT_BR = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
DIAS_ABREVIADOS_PT_BR = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

class SafeHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, firstweekday=calendar.SUNDAY, eventos_e_atividades=None, today=None):
        super().__init__(firstweekday)
        self.eventos_e_atividades = eventos_e_atividades or {}
        self.today = today
    
    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        
        css_classes = ['day']
        if day in self.eventos_e_atividades:
            compromissos = self.eventos_e_atividades[day]
            
            eventos = {c for c in compromissos if c[0] == 'evento'}
            atividades = {c for c in compromissos if c[0] != 'evento'}
            
            if eventos:
                css_classes.append('with-event')
                
            tipos_de_atividade = {act[0] for act in atividades}
            if len(tipos_de_atividade) > 1:
                css_classes.append('with-multiple-activities')
            elif len(tipos_de_atividade) == 1:
                tipo_unico = tipos_de_atividade.pop()
                css_classes.append(f'with-atividade-{tipo_unico}')

            posicoes = {act[1] for act in atividades if act[1]}
            if 'start' in posicoes:
                css_classes.append('with-activity-start')
            if 'middle' in posicoes:
                css_classes.append('with-activity-middle')
            if 'end' in posicoes:
                css_classes.append('with-activity-end')

        if self.today and self.today == day:
            css_classes.append('today')

        return f'<td class="{" ".join(css_classes)}">{day}</td>'

    def formatmonth(self, theyear, themonth, withyear=True):
        v = []
        a = v.append
        a(f'<table class="calendar-table" border="0" cellpadding="0" cellspacing="0">')
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
    
    def formatweekday(self, day):
        day_abbr = calendar.day_abbr[day].capitalize()
        return f'<th class="{self.cssclasses_weekday_head[day]}">{day_abbr}</th>'

    def formatweekheader(self):
        header_html = ''.join(f'<th>{day_name}</th>' for day_name in DIAS_ABREVIADOS_PT_BR)
        return f'<tr>{header_html}</tr>'

    def formatweek(self, theweek):
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return f'<tr>{s}</tr>'

@login_required
def agenda_view(request):
    docente_logado = request.user

    try:
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
    except (ValueError, TypeError):
        today = datetime.now()
        year, month = today.year, today.month

    prev_month, prev_year = (month - 1, year) if month > 1 else (12, year - 1)
    next_month, next_year = (month + 1, year) if month < 12 else (1, year + 1)
    
    current_year_for_range = datetime.now().year
    year_range = range(current_year_for_range - 5, current_year_for_range + 6)

    primeiro_dia_mes = date(year, month, 1)
    ultimo_dia_mes = primeiro_dia_mes + relativedelta(months=1) - timedelta(days=1)
    dias_marcados = {}

    eventos = Eventos.objects.filter(data__year=year, data__month=month, docente=docente_logado)
    for evento in eventos:
        dia = evento.data.day
        if dia not in dias_marcados: dias_marcados[dia] = set()
        dias_marcados[dia].add(('evento', None))

    modelos_map = {
        'pesquisa': AtividadePesquisa,
        'ensino': AtividadeEnsino,
        'extensao': AtividadeExtensao,
        'administracao': AtividadeAdministracao,
    }
    
    for tipo_str, modelo in modelos_map.items():
        atividades = modelo.objects.filter(
            id_docente=docente_logado,
            data_inicio__lte=ultimo_dia_mes,
            data_fim__gte=primeiro_dia_mes
        )
        
        for atividade in atividades:
            dia_atual = atividade.data_inicio
            while dia_atual <= atividade.data_fim:
                if dia_atual.year == year and dia_atual.month == month:
                    dia = dia_atual.day
                    if dia not in dias_marcados: dias_marcados[dia] = set()
                    
                    posicao = 'middle'
                    if dia_atual == atividade.data_inicio: posicao = 'start'
                    if dia_atual == atividade.data_fim: posicao = 'end'
                    if atividade.data_inicio == atividade.data_fim: posicao = 'single'

                    dias_marcados[dia].add((tipo_str, posicao))
                
                dia_atual += timedelta(days=1)

    today = None
    now = timezone.now().date()
    if now.year == year and now.month == month:
        today = now

    cal = SafeHTMLCalendar(eventos_e_atividades=dias_marcados, today=today)
    html_calendar = cal.formatmonth(year, month)
    month_name = MESES_PT_BR[month - 1]

    contexto = {
        'html_calendar': html_calendar,
        'current_year': year,
        'current_month_name': month_name,
        'current_month_number': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'active_page': 'agenda',
        'year_range': year_range,
    }
    return render(request, 'agenda/agenda.html', contexto)

@login_required
def atividades_view(request):
    docente_logado = request.user

    today = timezone.now().date()
    atividades_ativas = []

    selected_year = request.GET.get('year', 'all')
    items_per_page = int(request.GET.get('per_page', 5))
    selected_type = request.GET.get('tipo', 'all')
    sort_by = request.GET.get('sort', 'data_fim')
    direction = request.GET.get('direction', 'asc')

    activity_models = {
        'Pesquisa': (AtividadePesquisa, 'editar_atividade_pesquisa'),
        'Ensino': (AtividadeEnsino, 'editar_atividade_ensino'),
        'Extensão': (AtividadeExtensao, 'editar_atividade_extensao'),
        'Administração': (AtividadeAdministracao, 'editar_atividade_administracao'),
    }

    for tipo_geral, (model, url_name) in activity_models.items():
        if selected_type == 'all' or selected_type == tipo_geral:
            query = model.objects.filter(id_docente=docente_logado, data_fim__gte=today)
            if selected_year != 'all':
                query = query.filter(data_inicio__year=selected_year)

            for ativ in query:
                atividades_ativas.append({
                    'titulo': ativ.titulo,
                    'tipo_geral': tipo_geral,
                    'categoria': ativ.id_tipo.tipo,
                    'data_inicio': ativ.data_inicio,
                    'data_fim': ativ.data_fim,
                    'url_comprovante': ativ.comprovante.url if ativ.comprovante else None,
                    'url_edicao': reverse(url_name, args=[ativ.pk])
                })
    
    if direction not in ['asc', 'desc']:
        direction = 'asc'

    atividades_ativas.sort(key=itemgetter(sort_by), reverse=(direction == 'desc'))
    
    paginator = Paginator(atividades_ativas, items_per_page)
    page_number = request.GET.get('page')
    atividades_paginadas = paginator.get_page(page_number)

    years = set()
    for model in [AtividadePesquisa, AtividadeEnsino, AtividadeExtensao, AtividadeAdministracao]:
        years.update(model.objects.filter(id_docente=docente_logado).values_list('data_inicio__year', flat=True))
    
    contexto = {
        'active_page': 'atividades',
        'atividades_paginadas': atividades_paginadas,
        'available_years': sorted(list(filter(None, years)), reverse=True),
        'selected_year': selected_year,
        'items_per_page': items_per_page,
        'current_sort': sort_by,
        'current_direction': direction,
        'selected_type': selected_type,
    }

    return render(request, 'agenda/atividades.html', contexto)

@login_required
def cadastrar_atividade_view(request):
    docente_logado = request.user

    form_pesquisa = AtividadePesquisaForm()
    form_ensino = AtividadeEnsinoForm()
    form_extensao = AtividadeExtensaoForm()
    form_administracao = AtividadeAdministracaoForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'pesquisa':
            form_pesquisa = AtividadePesquisaForm(request.POST, request.FILES)
            if form_pesquisa.is_valid():
                nova_atividade = form_pesquisa.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Pesquisa cadastrada com sucesso!')
                return redirect('atividades')

        elif form_type == 'ensino':
            form_ensino = AtividadeEnsinoForm(request.POST, request.FILES)
            if form_ensino.is_valid():
                nova_atividade = form_ensino.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Ensino cadastrada com sucesso!')
                return redirect('atividades')
        
        elif form_type == 'extensao':
            form_extensao = AtividadeExtensaoForm(request.POST, request.FILES)
            if form_extensao.is_valid():
                nova_atividade = form_extensao.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Extensão cadastrada com sucesso!')
                return redirect('atividades')
            
        elif form_type == 'administracao':
            form_administracao = AtividadeAdministracaoForm(request.POST, request.FILES)
            if form_administracao.is_valid():
                nova_atividade = form_administracao.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Administração cadastrada com sucesso!')
                return redirect('atividades')

    contexto = {
        'active_page': 'atividades',
        'form_pesquisa': form_pesquisa,
        'form_ensino': form_ensino,
        'form_extensao': form_extensao,
        'form_administracao': form_administracao,
    }
    return render(request, 'agenda/cadastraratividade.html', contexto)

@login_required
def editar_atividade_pesquisa_view(request, id_atividadepesquisa):
    atividade = get_object_or_404(AtividadePesquisa, pk=id_atividadepesquisa)

    if request.method == 'POST':
        form = AtividadePesquisaForm(request.POST, request.FILES, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade de Pesquisa atualizada com sucesso!')
            return redirect('atividades')
    else:
        form = AtividadePesquisaForm(instance=atividade)

    contexto = {
        'form': form,
        'active_page': 'atividades',
        'tipo_atividade': 'Pesquisa',
    }
    return render(request, 'agenda/editaratividade.html', contexto)

@login_required
def editar_atividade_ensino_view(request, id_atividadeensino):
    atividade = get_object_or_404(AtividadeEnsino, pk=id_atividadeensino)
    if request.method == 'POST':
        form = AtividadeEnsinoForm(request.POST, request.FILES, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade de Ensino atualizada com sucesso!')
            return redirect('atividades')
    else:
        form = AtividadeEnsinoForm(instance=atividade)

    contexto = {
        'form': form,
        'active_page': 'atividades',
        'tipo_atividade': 'Ensino',
    }
    return render(request, 'agenda/editaratividade.html', contexto)

@login_required
def editar_atividade_extensao_view(request, id_atividadeextensao):
    atividade = get_object_or_404(AtividadeExtensao, pk=id_atividadeextensao)
    if request.method == 'POST':
        form = AtividadeExtensaoForm(request.POST, request.FILES, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade de Extensão atualizada com sucesso!')
            return redirect('atividades')
    else:
        form = AtividadeExtensaoForm(instance=atividade)

    contexto = {
        'form': form,
        'active_page': 'atividades',
        'tipo_atividade': 'Extensão',
    }
    return render(request, 'agenda/editaratividade.html', contexto)

@login_required
def editar_atividade_administracao_view(request, id_atividadeadministracao):
    atividade = get_object_or_404(AtividadeAdministracao, pk=id_atividadeadministracao)
    if request.method == 'POST':
        form = AtividadeAdministracaoForm(request.POST, request.FILES, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade de Administração atualizada com sucesso!')
            return redirect('atividades')
    else:
        form = AtividadeAdministracaoForm(instance=atividade)

    contexto = {
        'form': form,
        'active_page': 'atividades',
        'tipo_atividade': 'Administração',
    }
    return render(request, 'agenda/editaratividade.html', contexto)

@login_required
def excluir_atividade_pesquisa_view(request, id_atividadepesquisa):
    atividade = get_object_or_404(AtividadePesquisa, pk=id_atividadepesquisa)

    if request.method == 'POST':
        atividade.delete()
        messages.success(request, f'Atividade "{atividade.titulo}" foi excluída com sucesso!')
        return redirect('atividades')

    contexto = {
        'item': atividade,
        'tipo_item': 'Pesquisa',
        'active_page': 'atividades',
    }
    return render(request, 'agenda/confirmarexclusao.html', contexto)

@login_required
def excluir_atividade_ensino_view(request, id_atividadeensino):
    atividade = get_object_or_404(AtividadeEnsino, pk=id_atividadeensino)
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, f'Atividade "{atividade.titulo}" foi excluída com sucesso!')
        return redirect('atividades')

    contexto = {
        'item': atividade,
        'tipo_item': 'Ensino',
        'active_page': 'atividades',
    }
    return render(request, 'agenda/confirmarexclusao.html', contexto)

@login_required
def excluir_atividade_extensao_view(request, id_atividadeextensao):
    atividade = get_object_or_404(AtividadeExtensao, pk=id_atividadeextensao)
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, f'Atividade "{atividade.titulo}" foi excluída com sucesso!')
        return redirect('atividades')

    contexto = {
        'item': atividade,
        'tipo_item': 'Extensão',
        'active_page': 'atividades',
    }
    return render(request, 'agenda/confirmarexclusao.html', contexto)

@login_required
def excluir_atividade_administracao_view(request, id_atividadeadministracao):
    atividade = get_object_or_404(AtividadeAdministracao, pk=id_atividadeadministracao)
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, f'Atividade "{atividade.titulo}" foi excluída com sucesso!')
        return redirect('atividades')

    contexto = {
        'item': atividade,
        'tipo_item': 'Administração',
        'active_page': 'atividades',
    }
    return render(request, 'agenda/confirmarexclusao.html', contexto)

@login_required
def cadastrar_evento_view(request, ano, mes, dia):
    docente_logado = request.user
    data_inicial = datetime(ano, mes, dia, 8, 0).strftime('%Y-%m-%dT%H:%M')

    if request.method == 'POST':
        form = EventoForm(request.POST, docente=docente_logado)
        if form.is_valid():
            novo_evento = form.save(commit=False)
            novo_evento.docente = docente_logado

            atividade_selecionada = form.cleaned_data.get('atividade')
            if atividade_selecionada:
                content_type_id, object_id = atividade_selecionada.split('_')
                novo_evento.content_type_id = int(content_type_id)
                novo_evento.object_id = int(object_id)

            novo_evento.save()
            messages.success(request, 'Evento cadastrado com sucesso!')
            return redirect('agenda')
    else:
        form = EventoForm(initial={'data': data_inicial}, docente=docente_logado)

    contexto = {
        'form': form,
        'active_page': 'agenda',
    }
    return render(request, 'agenda/cadastrarevento.html', contexto)

@login_required
def eventos_list_view(request):
    sort_by = request.GET.get('sort', '-data')
    
    valid_sort_fields = ['titulo', 'data', 'atividade_relacionada__titulo']
    if sort_by.strip('-') not in valid_sort_fields:
        sort_by = '-data'

    eventos = Eventos.objects.filter(docente=request.user).order_by(sort_by)
    
    paginator = Paginator(eventos, 10)
    page_number = request.GET.get('page')
    eventos_paginados = paginator.get_page(page_number)
    
    contexto = {
        'active_page': 'eventos',
        'eventos_paginados': eventos_paginados,
        'current_sort': sort_by,
    }
    return render(request, 'agenda/eventoslista.html', contexto)

@login_required
def cadastrar_evento_geral_view(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, docente=request.user)
        if form.is_valid():
            novo_evento = form.save(commit=False)
            novo_evento.docente = request.user
            
            atividade_selecionada = form.cleaned_data.get('atividade')
            if atividade_selecionada:
                content_type_id, object_id = atividade_selecionada.split('_')
                novo_evento.content_type_id = int(content_type_id)
                novo_evento.object_id = int(object_id)

            novo_evento.save()
            messages.success(request, 'Novo evento cadastrado com sucesso!')
            return redirect('eventos_lista')
    else:
        form = EventoForm(docente=request.user)

    contexto = {
        'form': form, 
        'active_page': 'eventos'
    }
    return render(request, 'agenda/cadastrarevento.html', contexto)

@login_required
def editar_evento_view(request, id_evento):
    evento = get_object_or_404(Eventos, pk=id_evento, docente=request.user)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento, docente=request.user)
        if form.is_valid():
            evento_editado = form.save(commit=False)
            
            atividade_selecionada = form.cleaned_data.get('atividade')
            if atividade_selecionada:
                content_type_id, object_id = atividade_selecionada.split('_')
                evento_editado.content_type_id = int(content_type_id)
                evento_editado.object_id = int(object_id)
            else:
                evento_editado.content_type = None
                evento_editado.object_id = None

            evento_editado.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('eventos_lista')
    else:
        initial_data = {}
        if evento.atividade_relacionada:
            ct = ContentType.objects.get_for_model(evento.atividade_relacionada)
            initial_data['atividade'] = f'{ct.id}_{evento.object_id}'
        
        form = EventoForm(instance=evento, docente=request.user, initial=initial_data)

    contexto = {
        'form': form, 
        'active_page': 'eventos'
    }
    return render(request, 'agenda/cadastrarevento.html', contexto)

@login_required
def excluir_evento_view(request, id_evento):
    evento = get_object_or_404(Eventos, pk=id_evento)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, f'Evento "{evento.titulo}" foi excluído com sucesso!')
        return redirect('agenda')

    contexto = {
        'item': evento,
        'tipo_item': 'Evento',
    }
    return render(request, 'agenda/confirmarexclusao.html', contexto)

@login_required
def perfil_view(request):
    contexto = {
        'active_page': 'perfil'
    }
    return render(request, 'agenda/perfil.html', contexto)

@login_required
def editar_perfil_view(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)

    contexto = {
        'form': form,
        'active_page': 'perfil'
    }
    return render(request, 'agenda/editarperfil.html', contexto)

def register_view(request):
    if request.method == 'POST':
        form = DocenteRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}! Você já pode fazer o login.')
            return redirect('login')
    else:
        form = DocenteRegistrationForm()
    
    return render(request, 'login/registrar.html', {'form': form})

@login_required
def api_dados_dia_view(request, ano, mes, dia):
    data_selecionada = date(ano, mes, dia)
    dados = {
        'eventos': [],
        'atividades': []
    }

    docente_logado = request.user

    eventos = Eventos.objects.filter(data__date=data_selecionada, docente=docente_logado)
    for evento in eventos:
        dados['eventos'].append({
            'id': evento.id_evento,
            'titulo': evento.titulo,
            'descricao': evento.descricao,
            'atividade': str(evento.atividade_relacionada) if evento.atividade_relacionada else None,
            'hora': evento.data.strftime('%H:%M')
        })

    modelos_map = {
        'Pesquisa': AtividadePesquisa,
        'Ensino': AtividadeEnsino,
        'Extensão': AtividadeExtensao,
        'Administração': AtividadeAdministracao,
    }
    for tipo_str, modelo in modelos_map.items():
        atividades = modelo.objects.filter(
            id_docente=docente_logado,
            data_inicio__lte=data_selecionada,
            data_fim__gte=data_selecionada
        )
        for atividade in atividades:
            dados['atividades'].append({
                'titulo': atividade.titulo,
                'tipo': tipo_str
            })

    return JsonResponse(dados)

@login_required
def dashboard_view(request):
    docente_logado = request.user
    today = timezone.now().date()
    
    filter_option = request.GET.get('filter', 'all_time')
    
    start_date = None
    end_date = None

    if filter_option == 'last_7_days':
        start_date = today - timedelta(days=7)
        end_date = today
    elif filter_option == 'last_14_days':
        start_date = today - timedelta(days=14)
        end_date = today
    elif filter_option == 'last_month':
        start_date = today - relativedelta(months=1)
        end_date = today
    elif filter_option == 'last_year':
        start_date = today - relativedelta(years=1)
        end_date = today
    
    # Filtro de eventos
    eventos_query = Eventos.objects.filter(docente=docente_logado)
    if start_date and end_date:
        eventos_query = eventos_query.filter(data__range=[start_date, end_date])
    eventos_count = eventos_query.count()

    activity_models = {
        'Pesquisa': AtividadePesquisa, 'Ensino': AtividadeEnsino,
        'Extensão': AtividadeExtensao, 'Administração': AtividadeAdministracao,
    }
    activity_counts = {}
    total_activities_count = 0

    for name, model in activity_models.items():
        query = model.objects.filter(id_docente=docente_logado)
        if start_date and end_date:
            query = query.filter(data_inicio__range=[start_date, end_date])
        count = query.count()
        activity_counts[name] = count
        total_activities_count += count

    todas_as_atividades = []
    for model in activity_models.values():
        todas_as_atividades.extend(list(model.objects.filter(id_docente=docente_logado)))
    todas_as_atividades.sort(key=lambda x: x.data_inicio, reverse=True)
    atividades_recentes = todas_as_atividades[:5]

    proximos_eventos = Eventos.objects.filter(
        docente=docente_logado,
        data__gte=timezone.now()
    ).order_by('data')[:5]

    chart_data = {
        'labels': list(activity_counts.keys()),
        'data': list(activity_counts.values()),
    }

    contexto = {
        'active_page': 'dashboard',
        'eventos_count': eventos_count,
        'total_count': total_activities_count,
        'proximos_eventos': proximos_eventos,
        'atividades_recentes': atividades_recentes,
        'chart_data': json.dumps(chart_data),
        'current_filter': filter_option,
    }
    return render(request, 'agenda/dashboard.html', contexto)

@login_required
def historico_view(request):
    docente_logado = request.user
    selected_type = request.GET.get('tipo', 'all')
    sort_by = request.GET.get('sort', 'data_inicio')
    direction = request.GET.get('direction', 'desc')

    todas_as_atividades = []
    
    activity_models = {
        'Pesquisa': (AtividadePesquisa, 'editar_atividade_pesquisa'),
        'Ensino': (AtividadeEnsino, 'editar_atividade_ensino'),
        'Extensão': (AtividadeExtensao, 'editar_atividade_extensao'),
        'Administração': (AtividadeAdministracao, 'editar_atividade_administracao'),
    }

    for tipo_geral, (model, url_name) in activity_models.items():
        if selected_type == 'all' or selected_type == tipo_geral:
            query = model.objects.filter(id_docente=docente_logado)
            for ativ in query:
                todas_as_atividades.append({
                    'titulo': ativ.titulo,
                    'tipo_geral': tipo_geral,
                    'categoria': ativ.id_tipo.tipo,
                    'data_inicio': ativ.data_inicio,
                    'data_fim': ativ.data_fim,
                    'url_comprovante': ativ.comprovante.url if ativ.comprovante else None,
                    'url_edicao': reverse(url_name, args=[ativ.pk])
                })
    
    if direction not in ['asc', 'desc']:
        direction = 'desc'
    
    todas_as_atividades.sort(key=itemgetter(sort_by), reverse=(direction == 'desc'))

    paginator = Paginator(todas_as_atividades, 10)
    page_number = request.GET.get('page')
    atividades_paginadas = paginator.get_page(page_number)

    contexto = {
        'active_page': 'historico',
        'atividades_paginadas': atividades_paginadas,
        'current_sort': sort_by,
        'current_direction': direction,
        'selected_type': selected_type,
    }
    return render(request, 'agenda/historico.html', contexto)