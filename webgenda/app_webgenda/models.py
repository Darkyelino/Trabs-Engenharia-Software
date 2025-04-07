from django.db import models

class Docentes(models.Model):
    id_docente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

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
    aluno = models.CharField(max_length=255)
    data = models.DateTimeField()

class TipoPesquisa(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

class AtividadePesquisa(models.Model):
    id_atividadepesquisa = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_pesquisa')
    descricao = models.TextField()
    comprovante = models.FileField(upload_to='comprovantes/')
    id_tipo = models.ForeignKey('TipoPesquisa', on_delete=models.CASCADE, related_name='atividades_pesquisa')

class TipoEnsino(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

class AtividadeEnsino(models.Model):
    id_atividadeensino = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_ensino')
    descricao = models.TextField()
    comprovante = models.FileField(upload_to='comprovantes/')
    id_tipo = models.ForeignKey(TipoEnsino, on_delete=models.CASCADE, related_name='atividades_ensino')

class TipoExtensao(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

class AtividadeExtensao(models.Model):
    id_atividadeextensao = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_extensao')
    descricao = models.TextField()
    comprovante = models.FileField(upload_to='comprovantes/')
    id_tipo = models.ForeignKey(TipoExtensao, on_delete=models.CASCADE, related_name='atividades_extensao')

class TipoAdministracao(models.Model):
    id_tipoatividade = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

class AtividadeAdministracao(models.Model):
    id_atividadeadministracao = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docentes, on_delete=models.CASCADE, related_name='atividades_administracao')
    descricao = models.TextField()
    comprovante = models.FileField(upload_to='comprovantes/')
    id_tipo = models.ForeignKey(TipoAdministracao, on_delete=models.CASCADE, related_name='atividades_administracao')