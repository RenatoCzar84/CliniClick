from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password',
            'cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'telefone', 'cpf', 'data_nascimento', 'plano_saude'
        ]
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'password': 'Senha',
            'cep': 'CEP',
            'rua': 'Rua',
            'numero': 'Número',
            'complemento': 'Complemento (Bloco/Apartamento)',
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
            'complemento': forms.TextInput(attrs={'placeholder': 'Ex.: Bloco B, Apto 301'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna todos obrigatórios...
        for field in self.fields.values():
            field.required = True
        # ...exceto complemento (opcional)
        self.fields['complemento'].required = False

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        qs = Usuario.objects.filter(cpf=cpf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('password')
        if raw_password:
            user.set_password(raw_password)
        if commit:
            user.save()
        return user

widgets = {
    'password': forms.PasswordInput(),
    'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
    'complemento': forms.TextInput(attrs={'placeholder': 'Ex.: Bloco B, Apto 301'}),

    # força teclado numérico no mobile e restringe visualmente
    'cpf': forms.TextInput(attrs={
        'inputmode': 'numeric', 'pattern': r'\d*', 'maxlength': '14',
        'placeholder': '000.000.000-00'
    }),
    'telefone': forms.TextInput(attrs={
        'inputmode': 'numeric', 'pattern': r'\d*', 'maxlength': '15',
        'placeholder': '(00)00000-0000'
    }),
}
