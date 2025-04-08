from django.shortcuts import redirect, render, get_object_or_404
from .models import Docentes, Eventos, AtividadePesquisa, AtividadeEnsino, AtividadeExtensao, AtividadeAdministracao, TipoPesquisa, TipoEnsino, TipoAdministracao, TipoExtensao

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

    atividades = list(AtividadePesquisa.objects.filter(id_docente=docente)) + \
                 list(AtividadeEnsino.objects.filter(id_docente=docente)) + \
                 list(AtividadeExtensao.objects.filter(id_docente=docente)) + \
                 list(AtividadeAdministracao.objects.filter(id_docente=docente))

    return render(request, 'webgenda/atividades.html', {
        'docente': docente,
        'atividades': atividades
    })

def cad_atividadepesquisa(request):
    docente = get_object_or_404(Docentes, username='teste')  # Simulando login
    tipos = TipoPesquisa.objects.all()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        id_tipo = request.POST.get('id_tipo')
        comprovante = request.FILES.get('comprovante')

        tipo_obj = get_object_or_404(TipoPesquisa, pk=id_tipo)

        AtividadePesquisa.objects.create(
            id_docente=docente,
            titulo=titulo,
            descricao=descricao,
            comprovante=comprovante,
            id_tipo=tipo_obj
        )

        return redirect('cad_atividade')

    return render(request, 'webgenda/cad-atividadepesquisa.html', {
        'docente': docente,
        'tipos': tipos
    })