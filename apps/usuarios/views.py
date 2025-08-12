from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .forms import UsuarioForm

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # senha com hash no save() do form
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Verifique se CPF, e-mail ou usuário já estão em uso.")
                messages.error(request, "Não foi possível concluir o cadastro.")
            else:
                messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
                return redirect('usuarios:cadastro_sucesso')  # << AQUI COM NAMESPACE
        else:
            messages.error(request, "Há erros no formulário. Corrija e tente novamente.")
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


def cadastro_sucesso(request):
    return render(request, 'usuarios/cadastro_sucesso.html')


