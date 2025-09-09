from django import forms
from .models import AtividadePesquisa, AtividadeEnsino, AtividadeExtensao, AtividadeAdministracao

class AtividadePesquisaForm(forms.ModelForm):
    class Meta:
        model = AtividadePesquisa
        exclude = ['id_docente']
        labels = {
            'id_tipo': 'Tipo da Atividade',
        }
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

class AtividadeEnsinoForm(forms.ModelForm):
    class Meta:
        model = AtividadeEnsino
        exclude = ['id_docente']
        labels = {
            'id_tipo': 'Tipo da Atividade',
        }
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

class AtividadeExtensaoForm(forms.ModelForm):
    class Meta:
        model = AtividadeExtensao
        exclude = ['id_docente']
        labels = {
            'id_tipo': 'Tipo da Atividade',
        }
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

class AtividadeAdministracaoForm(forms.ModelForm):
    class Meta:
        model = AtividadeAdministracao
        exclude = ['id_docente']
        labels = {
            'id_tipo': 'Tipo da Atividade',
        }
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }