from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Docentes

@receiver(post_migrate)
def criar_dados_iniciais(sender, **kwargs):
    if not Docentes.objects.filter(username='teste').exists():
        Docentes.objects.create(
            nome='Docente Teste',
            username='teste',
            senha='123456',
            email='docente@teste.com'
        )
        print("Docente de teste criado.")
