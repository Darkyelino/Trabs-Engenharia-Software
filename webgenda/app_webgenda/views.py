from django.shortcuts import redirect, render, get_object_or_404
from .models import Docentes, Eventos, AtividadePesquisa, AtividadeEnsino, AtividadeExtensao, AtividadeAdministracao, TipoPesquisa, TipoEnsino, TipoAdministracao, TipoExtensao
from django.contrib import messages
from datetime import datetime
from django.db.models import Q

def home(request):
    # docente = get_object_or_404(Docentes, id=request.session['docente_id'])
    docente = get_object_or_404(Docentes, username='teste')

    eventos = Eventos.objects.filter(docente=docente)

    #"data;titulo;descricao|data;titulo;descricao"
    eventos_str = "|".join(
        f"{evento.data.strftime('%Y-%m-%d')};{evento.titulo};{evento.descricao}"
        for evento in eventos
    )

    context = {
        'docente': docente,
        'eventos_str': eventos_str
    }

    return render(request, 'webgenda/home.html', context)

def cad_docentes(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        # Verifica se já existe username ou email
        if Docentes.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
        elif Docentes.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já está em uso.')
        else:
            Docentes.objects.create(
                nome=nome,
                username=username,
                senha=senha,  # aqui seria ideal usar hash de senha depois
                email=email
            )
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')  # ou outra página após cadastro

    return render(request, 'webgenda/cad-docentes.html')

def adicionar_evento(request):
    if request.method == 'POST':
        docente = get_object_or_404(Docentes, username='teste')  # Simulando login
        data = request.POST.get('data')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        aluno = request.POST.get('aluno')

        # Criar o evento
        Eventos.objects.create(
            docente=docente,
            data=data,
            titulo=titulo,
            descricao=descricao,
            aluno=aluno
        )

    return redirect('home')

def atividades(request):
    docente = get_object_or_404(Docentes, username='teste')  # Simulando login

    query = request.GET.get('q', '').strip()
    atividades = []

    # Criar filtro se houver busca
    filtros = Q()
    if query:
        try:
            # Tenta converter a string para data
            data_query = datetime.strptime(query, "%d/%m/%Y")
            filtros |= Q(data_inicio__date=data_query.date()) | Q(data_fim__date=data_query.date())
        except ValueError:
            # Se não for data, busca por texto
            filtros |= Q(titulo__icontains=query) | Q(descricao__icontains=query)

    modelos = [
        ('pesquisa', AtividadePesquisa),
        ('ensino', AtividadeEnsino),
        ('extensao', AtividadeExtensao),
        ('administracao', AtividadeAdministracao),
    ]

    for tipo, modelo in modelos:
        atividades_qs = modelo.objects.filter(id_docente=docente)
        if query:
            atividades_qs = atividades_qs.filter(filtros)
        for atividade in atividades_qs:
            atividades.append({'obj': atividade, 'tipo': tipo})

    return render(request, 'webgenda/atividades.html', {
        'docente': docente,
        'atividades': atividades,
        'query': query,
    })

def cad_atividadepesquisa(request):
    docente = get_object_or_404(Docentes, username='teste')
    tipos = TipoPesquisa.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        id_tipo = request.POST.get('id_tipo')
        comprovante = request.FILES.get('comprovante')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        tipo_obj = get_object_or_404(TipoPesquisa, pk=id_tipo)
        AtividadePesquisa.objects.create(
            id_docente=docente,
            titulo=titulo,
            descricao=descricao,
            comprovante=comprovante,
            id_tipo=tipo_obj,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return redirect('atividades')
    return render(request, 'webgenda/cad-atividadepesquisa.html', {
        'docente': docente,
        'tipos': tipos
    })

def cad_atividadeensino(request):
    docente = get_object_or_404(Docentes, username='teste')
    tipos = TipoEnsino.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        id_tipo = request.POST.get('id_tipo')
        comprovante = request.FILES.get('comprovante')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        tipo_obj = get_object_or_404(TipoEnsino, pk=id_tipo)
        AtividadeEnsino.objects.create(
            id_docente=docente,
            titulo=titulo,
            descricao=descricao,
            comprovante=comprovante,
            id_tipo=tipo_obj,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return redirect('atividades')
    return render(request, 'webgenda/cad-atividadeensino.html', {
        'docente': docente,
        'tipos': tipos
    })

def cad_atividadeextensao(request):
    docente = get_object_or_404(Docentes, username='teste')
    tipos = TipoExtensao.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        id_tipo = request.POST.get('id_tipo')
        comprovante = request.FILES.get('comprovante')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        tipo_obj = get_object_or_404(TipoExtensao, pk=id_tipo)
        AtividadeExtensao.objects.create(
            id_docente=docente,
            titulo=titulo,
            descricao=descricao,
            comprovante=comprovante,
            id_tipo=tipo_obj,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return redirect('atividades')
    return render(request, 'webgenda/cad-atividadeextensao.html', {
        'docente': docente,
        'tipos': tipos
    })

def cad_atividadeadministracao(request):
    docente = get_object_or_404(Docentes, username='teste')
    tipos = TipoAdministracao.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        id_tipo = request.POST.get('id_tipo')
        comprovante = request.FILES.get('comprovante')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        tipo_obj = get_object_or_404(TipoAdministracao, pk=id_tipo)
        AtividadeAdministracao.objects.create(
            id_docente=docente,
            titulo=titulo,
            descricao=descricao,
            comprovante=comprovante,
            id_tipo=tipo_obj,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return redirect('atividades')
    return render(request, 'webgenda/cad-atividadeadministracao.html', {
        'docente': docente,
        'tipos': tipos
    })

def excluir_atividade(request, tipo, atividade_id):
    docente = get_object_or_404(Docentes, username='teste')

    modelos = {
        'pesquisa': AtividadePesquisa,
        'ensino': AtividadeEnsino,
        'extensao': AtividadeExtensao,
        'administracao': AtividadeAdministracao,
    }

    modelo = modelos.get(tipo)
    if not modelo:
        return redirect('atividades')

    atividade = get_object_or_404(modelo, pk=atividade_id, id_docente=docente)
    atividade.delete()
    return redirect('atividades')

def editar_atividade(request, tipo, atividade_id):
    docente = get_object_or_404(Docentes, username='teste')  # Simulando login

    modelos = {
        'pesquisa': AtividadePesquisa,
        'ensino': AtividadeEnsino,
        'extensao': AtividadeExtensao,
        'administracao': AtividadeAdministracao,
    }

    modelo = modelos.get(tipo)
    if not modelo:
        return redirect('atividades')

    atividade = get_object_or_404(modelo, pk=atividade_id, id_docente=docente)

    if request.method == 'POST':
        atividade.titulo = request.POST.get('titulo')
        atividade.descricao = request.POST.get('descricao')
        
        data_inicio_str = request.POST.get('data_inicio')
        data_fim_str = request.POST.get('data_fim')

        if data_inicio_str:
            atividade.data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        if data_fim_str:
            atividade.data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()

        if request.FILES.get('comprovante'):
            atividade.comprovante = request.FILES.get('comprovante')

        atividade.save()
        return redirect('atividades')

    return render(request, 'webgenda/editar_atividade.html', {
        'atividade': atividade,
        'tipo': tipo,
    })