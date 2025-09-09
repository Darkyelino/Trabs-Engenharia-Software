from django.contrib import admin
from .models import (
    Docentes,
    Administrador,
    Eventos,
    TipoPesquisa,
    AtividadePesquisa,
    TipoEnsino,
    AtividadeEnsino,
    TipoExtensao,
    AtividadeExtensao,
    TipoAdministracao,
    AtividadeAdministracao
)

admin.site.register(Docentes)
admin.site.register(Administrador)
admin.site.register(Eventos)
admin.site.register(TipoPesquisa)
admin.site.register(AtividadePesquisa)
admin.site.register(TipoEnsino)
admin.site.register(AtividadeEnsino)
admin.site.register(TipoExtensao)
admin.site.register(AtividadeExtensao)
admin.site.register(TipoAdministracao)
admin.site.register(AtividadeAdministracao)