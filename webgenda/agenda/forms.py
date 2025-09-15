from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

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

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError(
                    "A data de fim não pode ser anterior à data de início."
                )
        return cleaned_data

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

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError(
                    "A data de fim não pode ser anterior à data de início."
                )
        return cleaned_data

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

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError(
                    "A data de fim não pode ser anterior à data de início."
                )
        return cleaned_data

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

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError(
                    "A data de fim não pode ser anterior à data de início."
                )
        return cleaned_data

class EventoForm(forms.ModelForm):
    class Meta:
        model = Eventos
        exclude = ['docente']
        labels = {
            'titulo': 'Título do Evento',
            'aluno': 'Aluno (Opcional)',
        }
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Docentes
        fields = ['nome', 'username', 'email']

class DocenteRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Docentes
        fields = UserCreationForm.Meta.fields + ('nome', 'email',)
        labels = {
            'username': 'Nome de Usuário',
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'password1': 'Senha',
            'password2': 'Confirmação de Senha',
        }