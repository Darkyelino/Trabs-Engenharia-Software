from django.urls import path
from . import views

urlpatterns = [
    path('', views.agenda_view, name='agenda'),
    path('atividades/', views.atividades_view, name='atividades'),
    path('atividades/cadastrar/', views.cadastrar_atividade_view, name='cadastrar_atividade'),
    path('atividades/pesquisa/editar/<int:id_atividadepesquisa>/', views.editar_atividade_pesquisa_view, name='editar_atividade_pesquisa'),
    path('atividades/ensino/editar/<int:id_atividadeensino>/', views.editar_atividade_ensino_view, name='editar_atividade_ensino'),
    path('atividades/extensao/editar/<int:id_atividadeextensao>/', views.editar_atividade_extensao_view, name='editar_atividade_extensao'),
    path('atividades/administracao/editar/<int:id_atividadeadministracao>/', views.editar_atividade_administracao_view, name='editar_atividade_administracao'),
    path('atividades/pesquisa/excluir/<int:id_atividadepesquisa>/', views.excluir_atividade_pesquisa_view, name='excluir_atividade_pesquisa'),
    path('atividades/ensino/excluir/<int:id_atividadeensino>/', views.excluir_atividade_ensino_view, name='excluir_atividade_ensino'),
    path('atividades/extensao/excluir/<int:id_atividadeextensao>/', views.excluir_atividade_extensao_view, name='excluir_atividade_extensao'),
    path('atividades/administracao/excluir/<int:id_atividadeadministracao>/', views.excluir_atividade_administracao_view, name='excluir_atividade_administracao'),
    
    path('api/dados-dia/<int:ano>/<int:mes>/<int:dia>/', views.api_dados_dia_view, name='api_dados_dia'),
]