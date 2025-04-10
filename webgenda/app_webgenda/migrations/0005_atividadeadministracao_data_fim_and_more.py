# Generated by Django 5.1.7 on 2025-04-09 01:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_webgenda', '0004_atividadeadministracao_titulo_atividadeensino_titulo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividadeadministracao',
            name='data_fim',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadeadministracao',
            name='data_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadeensino',
            name='data_fim',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadeensino',
            name='data_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadeextensao',
            name='data_fim',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadeextensao',
            name='data_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadepesquisa',
            name='data_fim',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadepesquisa',
            name='data_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
