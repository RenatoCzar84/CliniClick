# forms.py
from django import forms
from .models import Medico

class AgendamentoConsultaForm(forms.Form):
    especialidade_desejada = forms.ChoiceField(
        label="Especialidade Desejada",
        required=True,
        choices=[],  # deixamos vazio e setamos na view
        widget=forms.Select(attrs={'id': 'id_especialidade', 'class': 'form-control'})
    )
    medico = forms.ModelChoiceField(
        queryset=Medico.objects.none(),  # inicial vazio
        label="Escolha o Médico",
        empty_label="--- Selecione um Médico ---",
        required=True,
        widget=forms.Select(attrs={'id': 'id_medico', 'class': 'form-control'})
    )
