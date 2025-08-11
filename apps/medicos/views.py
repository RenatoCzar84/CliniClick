from django.shortcuts import render
from .models import Especialidade, Medico

def medicos_especialidades(request):
    especialidade_id = request.GET.get('especialidade')
    medico_id = request.GET.get('medico')

    especialidades = Especialidade.objects.all()
    medicos = Medico.objects.none()  # padrão: nenhum médico

    if especialidade_id:
        medicos = Medico.objects.filter(especialidade_id=especialidade_id)

    sucesso = False
    if especialidade_id and medico_id:
        sucesso = True

    context = {
        'especialidades': especialidades,
        'medicos': medicos,
        'especialidade_selecionada': especialidade_id,
        'medico_selecionado': medico_id,
        'sucesso': sucesso
    }

    return render(request, 'medicos/medicos_especialidades.html', context)

