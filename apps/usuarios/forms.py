from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario
import re

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
            # não reapresenta a senha após erro de validação
            'password': forms.PasswordInput(render_value=False),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'complemento': forms.TextInput(attrs={'placeholder': 'Ex.: Bloco B, Apto 301'}),

            # reforça teclado numérico no mobile
            'cpf': forms.TextInput(attrs={
                'inputmode': 'numeric', 'maxlength': '14', 'placeholder': '000.000.000-00'
            }),
            'telefone': forms.TextInput(attrs={
                'inputmode': 'numeric', 'maxlength': '15', 'placeholder': '(00)00000-0000'
            }),
            'cep': forms.TextInput(attrs={
                'inputmode': 'numeric', 'maxlength': '9', 'placeholder': '00000-000'
            }),
        }

    # ===== utilitários =====
    @staticmethod
    def _so_digitos(valor: str) -> str:
        return re.sub(r'\D', '', valor or '')

    @staticmethod
    def _cpf_valido(cpf_digits: str) -> bool:
        if len(cpf_digits) != 11 or cpf_digits == cpf_digits[0] * 11:
            return False
        def dv(nums: str, peso_ini: int) -> int:
            soma = sum(int(n) * p for n, p in zip(nums, range(peso_ini, 1, -1)))
            r = (soma * 10) % 11
            return 0 if r == 10 else r
        d1 = dv(cpf_digits[:9], 10)
        d2 = dv(cpf_digits[:9] + str(d1), 11)
        return cpf_digits.endswith(f"{d1}{d2}")

    # ===== required / optional + AUTOCOMPLETE OFF =====
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.required = True
            # desativa autocomplete no input
            field.widget.attrs['autocomplete'] = 'off'

        # dicas específicas reconhecidas pelos navegadores
        if 'username' in self.fields:
            self.fields['username'].widget.attrs['autocomplete'] = 'username'
        if 'email' in self.fields:
            self.fields['email'].widget.attrs['autocomplete'] = 'email'
        if 'password' in self.fields:
            self.fields['password'].widget.attrs['autocomplete'] = 'new-password'

        # exceção: complemento é opcional
        self.fields['complemento'].required = False

    # ===== cleans =====
    def clean_first_name(self):
        nome = (self.cleaned_data.get('first_name') or '').strip()
        if not re.fullmatch(r"[A-Za-zÀ-ÿ ]+", nome):
            raise ValidationError("Use apenas letras e espaços no Nome.")
        return nome

    def clean_last_name(self):
        sobrenome = (self.cleaned_data.get('last_name') or '').strip()
        if not re.fullmatch(r"[A-Za-zÀ-ÿ ]+", sobrenome):
            raise ValidationError("Use apenas letras e espaços no Sobrenome.")
        return sobrenome

    def clean_cpf(self):
        cpf = self._so_digitos(self.cleaned_data.get('cpf'))
        if not self._cpf_valido(cpf):
            raise ValidationError("CPF inválido.")
        qs = Usuario.objects.filter(cpf=cpf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf  # salva só dígitos

    def clean_telefone(self):
        tel = self._so_digitos(self.cleaned_data.get('telefone'))
        if len(tel) not in (10, 11):
            raise ValidationError("Telefone deve ter DDD + número (10 ou 11 dígitos).")
        return tel

    def clean_cep(self):
        cep = self._so_digitos(self.cleaned_data.get('cep'))
        if len(cep) != 8:
            raise ValidationError("CEP deve ter 8 dígitos.")
        return cep

    def clean_estado(self):
        uf = (self.cleaned_data.get('estado') or '').strip().upper()
        if len(uf) != 2 or not uf.isalpha():
            raise ValidationError("Estado deve ser a sigla com 2 letras (ex.: SP, RJ).")
        return uf

    # ===== save com hash de senha =====
    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('password')
        if raw_password:
            user.set_password(raw_password)  # hash seguro
        # normaliza campos
        user.cpf = self._so_digitos(getattr(user, 'cpf', ''))
        user.cep = self._so_digitos(getattr(user, 'cep', ''))
        user.telefone = self._so_digitos(getattr(user, 'telefone', ''))
        user.estado = (getattr(user, 'estado', '') or '').upper()
        if commit:
            user.save()
        return user
