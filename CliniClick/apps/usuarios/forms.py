from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Usuario

cpf_validator = RegexValidator(
    regex=r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
    message='Informe um CPF válido (apenas números ou no formato 000.000.000-00).'
)

class UsuarioForm(forms.ModelForm):
    # Campos de senha com confirmação
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    cpf = forms.CharField(
        label='CPF',
        validators=[cpf_validator],
        help_text='Use apenas números ou o formato 000.000.000-00.'
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password', 'password2',
            'cep', 'logradouro', 'bairro', 'cidade', 'estado',
            'telefone', 'cpf', 'data_nascimento', 'plano_saude'
        ]
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
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
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        # Normaliza removendo pontuação para checar unicidade com mais robustez
        cpf_normalizado = ''.join([c for c in cpf if c.isdigit()])
        # Procura por duplicata considerando os dois jeitos de salvar
        if (Usuario.objects.filter(cpf=cpf).exists() or
            Usuario.objects.filter(cpf=cpf_normalizado).exists()):
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean(self):
        data = super().clean()
        p1 = data.get('password')
        p2 = data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'As senhas não conferem.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Garante que a senha seja armazenada com hash
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UsuarioProfileForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False, label='Email')
    cpf = forms.CharField(disabled=True, required=False, label='CPF')

    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'email', 'telefone', 'cpf',
            'data_nascimento', 'foto',
            'cep', 'logradouro', 'bairro', 'cidade', 'estado',
            'plano_saude'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'foto': forms.ClearableFileInput(),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'telefone': 'Telefone',
            'data_nascimento': 'Data de nascimento',
            'foto': 'Foto de perfil',
            'cep': 'CEP',
            'logradouro': 'Logradouro',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'plano_saude': 'Plano de Saúde',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só exibimos email/cpf como leitura; não serão enviados/salvos
        self.fields['email'].help_text = 'Este e-mail não pode ser alterado.'
        self.fields['cpf'].help_text = 'Este CPF não pode ser alterado.'

