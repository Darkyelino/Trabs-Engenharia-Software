from django.db import models

class Docentes(models.Model):
    id_docente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
