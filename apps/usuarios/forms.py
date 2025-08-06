from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password',
            'cep', 'logradouro', 'bairro', 'cidade', 'estado',
            'telefone', 'cpf', 'data_nascimento', 'plano_saude'
        ]
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'password': 'Senha',
            'cep': 'CEP',
            'logradouro': 'Logradouro',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'telefone': 'Telefone',
            'cpf': 'CPF',
            'data_nascimento': 'Data de nascimento',
            'plano_saude': 'Plano de Saúde',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Usuario.objects.filter(cpf=cpf).exists():
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf