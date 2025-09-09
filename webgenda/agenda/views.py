from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import calendar
from datetime import date, datetime, timedelta
import locale
import sys

class SafeHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, firstweekday=calendar.SUNDAY, eventos_e_atividades=None):
        super().__init__(firstweekday)
        self.eventos_e_atividades = eventos_e_atividades or {}
    
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
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return f'<tr>{s}</tr>'

    def formatweek(self, theweek):
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return f'<tr>{s}</tr>'

@login_required
def agenda_view(request):
    docente_logado = request.user

    if sys.platform.startswith('win'):
        locale_str = 'ptb'
    else:
        locale_str = 'pt_BR.UTF-8'
    try:
        locale.setlocale(locale.LC_TIME, locale_str)
    except locale.Error:
        locale.setlocale(locale.LC_TIME, '')

    try:
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
    except (ValueError, TypeError):
        today = datetime.now()
        year = today.year
        month = today.month

    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year = year + 1

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
            data_inicio__year__lte=year,
            data_fim__year__gte=year
        ).filter(
            data_inicio__month__lte=month,
            data_fim__month__gte=month
        )
        
        for atividade in atividades:
            delta = atividade.data_fim - atividade.data_inicio
            for i in range(delta.days + 1):
                dia_atual = atividade.data_inicio + timedelta(days=i)
                if dia_atual.year == year and dia_atual.month == month:
                    dia = dia_atual.day
                    if dia not in dias_marcados: dias_marcados[dia] = set()

                    posicao = 'middle'
                    if i == 0: posicao = 'start'
                    if i == delta.days: posicao = 'end'
                    if delta.days == 0: posicao = 'single'

                    dias_marcados[dia].add((tipo_str, posicao))

    cal = SafeHTMLCalendar(eventos_e_atividades=dias_marcados)
    
    html_calendar = cal.formatmonth(year, month)
    month_name = calendar.month_name[month].capitalize()

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
    }
    return render(request, 'agenda/agenda.html', contexto)

@login_required
def atividades_view(request):
    docente_logado = request.user

    atividades_pesquisa = AtividadePesquisa.objects.filter(id_docente=docente_logado).order_by('-data_inicio')
    atividades_ensino = AtividadeEnsino.objects.filter(id_docente=docente_logado).order_by('-data_inicio')
    atividades_extensao = AtividadeExtensao.objects.filter(id_docente=docente_logado).order_by('-data_inicio')
    atividades_administracao = AtividadeAdministracao.objects.filter(id_docente=docente_logado).order_by('-data_inicio')

    pesquisa_count = atividades_pesquisa.count()
    ensino_count = atividades_ensino.count()
    extensao_count = atividades_extensao.count()
    admin_count = atividades_administracao.count()
    total_count = pesquisa_count + ensino_count + extensao_count + admin_count

    contexto = {
        'active_page': 'atividades',
        'atividades_pesquisa': atividades_pesquisa,
        'atividades_ensino': atividades_ensino,
        'atividades_extensao': atividades_extensao,
        'atividades_administracao': atividades_administracao,
        'pesquisa_count': pesquisa_count,
        'ensino_count': ensino_count,
        'extensao_count': extensao_count,
        'admin_count': admin_count,
        'total_count': total_count,
    }

    return render(request, 'agenda/atividades.html', contexto)

@login_required
def cadastrar_atividade_view(request):
    docente_logado = request.user

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'pesquisa':
            form = AtividadePesquisaForm(request.POST, request.FILES)
            if form.is_valid():
                nova_atividade = form.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Pesquisa cadastrada com sucesso!')
                return redirect('atividades')

        elif form_type == 'ensino':
            form = AtividadeEnsinoForm(request.POST, request.FILES)
            if form.is_valid():
                nova_atividade = form.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Ensino cadastrada com sucesso!')
                return redirect('atividades')
        
        elif form_type == 'extensao':
            form = AtividadeExtensaoForm(request.POST, request.FILES)
            if form.is_valid():
                nova_atividade = form.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Extensão cadastrada com sucesso!')
                return redirect('atividades')
            
        elif form_type == 'administracao':
            form = AtividadeAdministracaoForm(request.POST, request.FILES)
            if form.is_valid():
                nova_atividade = form.save(commit=False)
                nova_atividade.id_docente = docente_logado
                nova_atividade.save()
                messages.success(request, 'Atividade de Administração cadastrada com sucesso!')
                return redirect('atividades')

    form_pesquisa = AtividadePesquisaForm()
    form_ensino = AtividadeEnsinoForm()
    form_extensao = AtividadeExtensaoForm()
    form_administracao = AtividadeAdministracaoForm()

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
        form = EventoForm(request.POST)
        if form.is_valid():
            novo_evento = form.save(commit=False)
            novo_evento.docente = docente_logado
            novo_evento.save()
            messages.success(request, 'Evento cadastrado com sucesso!')
            return redirect('agenda')
    else:
        form = EventoForm(initial={'data': data_inicial})

    contexto = {
        'form': form,
        'active_page': 'agenda',
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


@login_required
def api_dados_dia_view(request, ano, mes, dia):
    data_selecionada = date(ano, mes, dia)
    dados = {
        'eventos': [],
        'atividades': []
    }

    eventos = Eventos.objects.filter(data__date=data_selecionada)
    for evento in eventos:
        dados['eventos'].append({
            'id': evento.id_evento,
            'titulo': evento.titulo,
            'descricao': evento.descricao,
            'aluno': evento.aluno
        })

    modelos_de_atividade = [AtividadePesquisa, AtividadeEnsino, AtividadeExtensao, AtividadeAdministracao]
    for modelo in modelos_de_atividade:
        atividades = modelo.objects.filter(data_inicio__lte=data_selecionada, data_fim__gte=data_selecionada)
        for atividade in atividades:
            dados['atividades'].append({
                'titulo': atividade.titulo,
                'tipo': modelo._meta.verbose_name.title()
            })

    return JsonResponse(dados)