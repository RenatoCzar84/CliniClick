from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

Usuario = get_user_model()

NOME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$")

def somente_digitos(s: str) -> str:
    return re.sub(r"\D+", "", s or "")

def validar_cpf(cpf: str) -> bool:
    cpf = somente_digitos(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    # dígitos verificadores
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11
    d1 = 0 if d1 == 10 else d1
    if d1 != int(cpf[9]):
        return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11
    d2 = 0 if d2 == 10 else d2
    return d2 == int(cpf[10])

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"})
    )

    class Meta:
        model = Usuario
        fields = [
            "username", "first_name", "last_name", "email",
            "cep", "rua", "numero", "complemento", "bairro", "cidade", "estado",
            "telefone", "cpf", "data_nascimento", "plano_saude", "apelido",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "id": "id_first_name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "id": "id_last_name"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "cep": forms.TextInput(attrs={"class": "form-control", "id": "id_cep"}),
            "rua": forms.TextInput(attrs={"class": "form-control", "id": "id_rua"}),
            "numero": forms.TextInput(attrs={"class": "form-control", "id": "id_numero"}),
            "complemento": forms.TextInput(attrs={"class": "form-control", "id": "id_complemento"}),
            "bairro": forms.TextInput(attrs={"class": "form-control", "id": "id_bairro"}),
            "cidade": forms.TextInput(attrs={"class": "form-control", "id": "id_cidade"}),
            "estado": forms.TextInput(attrs={"class": "form-control", "maxlength": 2, "id": "id_estado"}),
            "telefone": forms.TextInput(attrs={"class": "form-control", "id": "id_telefone"}),
            "cpf": forms.TextInput(attrs={"class": "form-control", "id": "id_cpf"}),
            "data_nascimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "plano_saude": forms.TextInput(attrs={"class": "form-control"}),
            "apelido": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_first_name(self):
        v = (self.cleaned_data.get("first_name") or "").strip()
        if not NOME_REGEX.match(v):
            raise ValidationError("Use apenas letras e espaços em Nome.")
        return v

    def clean_last_name(self):
        v = (self.cleaned_data.get("last_name") or "").strip()
        if not NOME_REGEX.match(v):
            raise ValidationError("Use apenas letras e espaços em Sobrenome.")
        return v

    def clean_cpf(self):
        cpf = somente_digitos(self.cleaned_data.get("cpf"))
        if not validar_cpf(cpf):
            raise ValidationError("CPF inválido.")
        # unicidade via formulário
        qs = Usuario.objects.filter(cpf=cpf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Já existe um usuário com este CPF.")
        return cpf  # salvo normalizado

    def clean_telefone(self):
        tel = somente_digitos(self.cleaned_data.get("telefone"))
        if len(tel) not in (10, 11):
            raise ValidationError("Telefone deve ter 10 ou 11 dígitos.")
        return tel

    def clean_cep(self):
        cep = somente_digitos(self.cleaned_data.get("cep"))
        if len(cep) != 8:
            raise ValidationError("CEP deve ter 8 dígitos.")
        return cep

    def clean_estado(self):
        uf = (self.cleaned_data.get("estado") or "").strip().upper()
        if len(uf) != 2 or not uf.isalpha():
            raise ValidationError("UF deve ter 2 letras (ex.: SP).")
        return uf

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não conferem.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        # garantir normalização também aqui (caso venha por API)
        user.cpf = somente_digitos(self.cleaned_data.get("cpf"))
        user.telefone = somente_digitos(self.cleaned_data.get("telefone"))
        user.cep = somente_digitos(self.cleaned_data.get("cep"))
        user.estado = (self.cleaned_data.get("estado") or "").upper()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
