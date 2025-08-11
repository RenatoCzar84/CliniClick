from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import PacienteRegistrationForm
from .models import Consulta

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lista_consultas')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def lista_consultas(request):
    user = request.user
    consultas = Consulta.objects.none()  # Inicializa vazio
    
    if hasattr(user, 'paciente'):
        consultas = Consulta.objects.filter(paciente=user.paciente)
    elif hasattr(user, 'medico'):
        consultas = Consulta.objects.filter(medico=user.medico)
    
    return render(request, 'lista_consultas.html', {'consultas': consultas})

@login_required
def detalhe_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    
    # Verifica permissão corretamente
    user = request.user
    if not (hasattr(user, 'medico') and not (hasattr(user, 'paciente') and user.paciente == consulta.paciente)):
        return redirect('home')
    
    return render(request, 'detalhe_consulta.html', {'consulta': consulta})

def registro_paciente(request):
    if request.method == 'POST':
        form = PacienteRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Autentica o usuário automaticamente após registro
            login(request, user)
            return redirect('lista_consultas')
    else:
        form = PacienteRegistrationForm()
    return render(request, 'registro_paciente.html', {'form': form})