from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Docentes(AbstractUser):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome or self.username

class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

class Eventos(models.Model):
    id_evento = models.AutoField(primary_key=True)
    docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='eventos')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    atividade_relacionada = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.titulo


class TipoPesquisa(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

class AtividadePesquisa(models.Model):
    id_atividadepesquisa = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_pesquisa')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    id_tipo = models.ForeignKey('TipoPesquisa', on_delete=models.CASCADE, related_name='atividades_pesquisa')

class TipoEnsino(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

class AtividadeEnsino(models.Model):
    id_atividadeensino = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_ensino')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    id_tipo = models.ForeignKey(TipoEnsino, on_delete=models.CASCADE, related_name='atividades_ensino')

class TipoExtensao(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

class AtividadeExtensao(models.Model):
    id_atividadeextensao = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_extensao')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    id_tipo = models.ForeignKey(TipoExtensao, on_delete=models.CASCADE, related_name='atividades_extensao')

class TipoAdministracao(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

class AtividadeAdministracao(models.Model):
    id_atividadeadministracao = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_administracao')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    id_tipo = models.ForeignKey(TipoAdministracao, on_delete=models.CASCADE, related_name='atividades_administracao')