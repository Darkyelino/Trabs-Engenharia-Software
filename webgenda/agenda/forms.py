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
    atividade = forms.ChoiceField(label="Atividade Relacionada (Opcional)", required=False)

    class Meta:
        model = Eventos
        fields = ['titulo', 'descricao', 'data', 'atividade']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        docente = kwargs.pop('docente', None)
        super().__init__(*args, **kwargs)

        if docente:
            choices = [('', '---------')]
            activity_models = {
                'Pesquisa': AtividadePesquisa,
                'Ensino': AtividadeEnsino,
                'Extensão': AtividadeExtensao,
                'Administração': AtividadeAdministracao,
            }
            for model_name, model in activity_models.items():
                atividades = model.objects.filter(id_docente=docente)
                for ativ in atividades:
                    content_type = ContentType.objects.get_for_model(model)
                    choices.append(
                        (f'{content_type.id}_{ativ.pk}', f'{model_name}: {ativ.titulo}')
                    )
            self.fields['atividade'].choices = choices

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