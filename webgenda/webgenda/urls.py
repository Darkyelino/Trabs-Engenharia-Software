"""
URL configuration for webgenda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_webgenda import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('adicionar-evento/', views.adicionar_evento, name='adicionar_evento'),
    path('atividades/', views.atividades, name='atividades'),
    path('atividades/pesquisa-cadastrar/', views.cad_atividadepesquisa, name='cad_atividadepesquisa'),
    path('atividades/ensino-cadastrar/', views.cad_atividadeensino, name='cad_atividadeensino'),
    path('atividades/extensao-cadastrar/', views.cad_atividadeextensao, name='cad_atividadeextensao'),
    path('atividades/administracao-cadastrar/', views.cad_atividadeadministracao, name='cad_atividadeadministracao'),
    path('atividades/editar/<str:tipo>/<int:atividade_id>/', views.editar_atividade, name='editar_atividade'),
    path('atividades/excluir/<str:tipo>/<int:atividade_id>/', views.excluir_atividade, name='excluir_atividade'),
    path('cadastro/docente/', views.cad_docentes, name='cad_docentes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)