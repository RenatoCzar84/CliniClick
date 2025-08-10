from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuario

cpf_validator = RegexValidator(
    regex=r'^(?:\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2})$',
    message=_('Informe um CPF válido (somente números ou 000.000.000-00).')
)

telefone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message=_('Informe um telefone válido (apenas números, com DDD; opcionalmente com +código do país).')
)

def _normaliza_cpf(valor: str) -> str:
    if not valor:
        return valor
    return valor.replace('.', '').replace('-', '').strip()


class UsuarioSignupForm(UserCreationForm):
    # Campos extras (UserCreationForm já traz password1/password2)
    first_name = forms.CharField(label='Nome', max_length=150, required=True)
    last_name = forms.CharField(label='Sobrenome', max_length=150, required=True)
    email = forms.EmailField(label='Email', required=True)

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        validators=[cpf_validator],
        required=True
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        required=False,
        validators=[telefone_validator]
    )
    data_nascimento = forms.DateField(
        label='Data de nascimento',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    cep = forms.CharField(label='CEP', max_length=10, required=False)
    logradouro = forms.CharField(label='Logradouro', max_length=100, required=False)
    bairro = forms.CharField(label='Bairro', max_length=100, required=False)
    cidade = forms.CharField(label='Cidade', max_length=100, required=False)
    estado = forms.CharField(label='Estado', max_length=2, required=False)
    plano_saude = forms.CharField(label='Plano de Saúde', max_length=100, required=False)

    foto = forms.ImageField(label='Foto de perfil', required=False)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2',
            'cpf', 'telefone', 'data_nascimento',
            'cep', 'logradouro', 'bairro', 'cidade', 'estado', 'plano_saude',
            'foto',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Este email já está cadastrado.')
        return email

    def clean_cpf(self):
        cpf = _normaliza_cpf(self.cleaned_data.get('cpf', ''))
        if not cpf:
            raise ValidationError('CPF é obrigatório.')
        if Usuario.objects.filter(cpf__in=[cpf, self.cleaned_data.get('cpf')]).exists():
            # cobre tanto 00000000000 quanto 000.000.000-00
            raise ValidationError('Este CPF já está cadastrado.')
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)  # UserCreationForm cuida do hash da senha
        user.email = self.cleaned_data['email'].lower().strip()
        user.cpf = self.cleaned_data['clean_cpf'] if 'clean_cpf' in self.cleaned_data else self.cleaned_data['cpf']
        # garantir cpf normalizado
        user.cpf = _normaliza_cpf(user.cpf)

        # Demais campos extras
        user.telefone = self.cleaned_data.get('telefone', '')
        user.data_nascimento = self.cleaned_data.get('data_nascimento')
        user.cep = self.cleaned_data.get('cep', '')
        user.logradouro = self.cleaned_data.get('logradouro', '')
        user.bairro = self.cleaned_data.get('bairro', '')
        user.cidade = self.cleaned_data.get('cidade', '')
        user.estado = self.cleaned_data.get('estado', '')
        user.plano_saude = self.cleaned_data.get('plano_saude', '')

        if commit:
            user.save()
            foto = self.cleaned_data.get('foto')
            if foto:
                user.foto = foto
                user.save(update_fields=['foto'])
        return user


class UsuarioProfileForm(UserChangeForm):
    password = None  # esconde o campo password do UserChangeForm

    email = forms.EmailField(label='Email', required=True, disabled=True)
    cpf = forms.CharField(label='CPF', required=True, disabled=True)

    data_nascimento = forms.DateField(
        label='Data de nascimento',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        required=False,
        validators=[telefone_validator]
    )
    foto = forms.ImageField(label='Foto de perfil', required=False)

    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name',
            'email', 'cpf',                # somente leitura
            'telefone', 'data_nascimento',
            'cep', 'logradouro', 'bairro', 'cidade', 'estado',
            'plano_saude',
            'foto',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deixar CPF/e-mail bloqueados para edição
        self.fields['email'].disabled = True
        self.fields['cpf'].disabled = True

    def clean_cpf(self):
        # mantém o CPF atual (não deixa alterar)
        return self.instance.cpf
