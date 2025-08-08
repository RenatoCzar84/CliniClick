
from django import forms
from .models import Medico

class AgendamentoConsultaForm(forms.Form):
    especialidade_desejada = forms.CharField(
        label="Especialidade Desejada",
        required=True,
        widget=forms.Select(attrs={'id': 'id_especialidade', 'class': 'form-control'})
    )
    medico = forms.ModelChoiceField(
        queryset=Medico.objects.all(),
        label="Escolha o Médico",
        empty_label="--- Selecione um Médico ---",
        required=True,
        widget=forms.Select(attrs={'id': 'id_medico', 'class': 'form-control'})
    )