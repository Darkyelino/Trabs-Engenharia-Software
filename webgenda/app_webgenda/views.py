from django.shortcuts import redirect, render, get_object_or_404
from .models import Docentes, Eventos

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
