from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import UsuarioForm

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                print("Formulário VÁLIDO")
                form.save()
                return redirect('cadastro_sucesso')
            except IntegrityError as e:
                form.add_error(None, "Erro ao salvar os dados. Verifique se o CPF, email ou nome de usuário já está em uso.")
                print("Erro de integridade:", e)
        else:
            print("Formulário INVÁLIDO:", form.errors)
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

def cadastro_sucesso(request):
    return render(request, 'usuarios/cadastro_sucesso.html')
