

import json
from django.shortcuts import render
from .models import Medico
from .forms import AgendamentoConsultaForm

def medicos_e_especialidades(request):
    especialidades = Medico.objects.values_list('especialidade', flat=True).distinct()
    choices = [('', '--- Selecione uma Especialidade ---')] + [(e, e) for e in especialidades]
    
    form = AgendamentoConsultaForm()
    form.fields['especialidade_desejada'].choices = choices

    medicos_por_especialidade = {}
    for medico in Medico.objects.all():
        if medico.especialidade not in medicos_por_especialidade:
            medicos_por_especialidade[medico.especialidade] = []
        medicos_por_especialidade[medico.especialidade].append({
            'id': medico.id,
            'nome': medico.nome,
            'crm': medico.crm,
        })
    medicos_json = json.dumps(medicos_por_especialidade)

    contexto = {
        'form': form,
        'medicos_json': medicos_json,
    }
    
    return render(request, 'medicos/medicos_especialidades.html', contexto)