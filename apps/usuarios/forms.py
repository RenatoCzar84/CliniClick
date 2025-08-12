from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    """
    Formulário de login com classes Bootstrap.
    """
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seu usuário',
            'autofocus': 'autofocus',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Sua senha',
            'autocomplete': 'current-password',
        })


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Crie uma senha segura',
        })
    )

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
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # adiciona classe Bootstrap a todos os campos (menos o password que já tem acima)
        for name, field in self.fields.items():
            if name != 'password':
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (existing + ' form-control').strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and Usuario.objects.filter(cpf=cpf).exists():
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf

    def save(self, commit=True):
        """
        Garante que a senha seja salva com hash.
        """
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
