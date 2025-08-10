from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

cpf_validator = RegexValidator(
    regex=r'^(?:\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2})$',
    message=_('Informe um CPF válido (somente números ou no formato 000.000.000-00).')
)

telefone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message=_('Informe um telefone válido (apenas números, com DDD; opcionalmente com +código do país).')
)

class Usuario(AbstractUser):
    # Campos de perfil
    cpf = models.CharField(
        _('CPF'),
        max_length=14,
        unique=True,
        validators=[cpf_validator],
        blank=False,
        null=False,
        help_text=_('CPF único do usuário (somente números ou 000.000.000-00).')
    )
    telefone = models.CharField(
        _('Telefone'),
        max_length=20,
        blank=True,
        validators=[telefone_validator]
    )
    data_nascimento = models.DateField(
        _('Data de nascimento'),
        null=True,
        blank=True
    )

    
    cep = models.CharField(_('CEP'), max_length=10, blank=True)
    logradouro = models.CharField(_('Logradouro'), max_length=100, blank=True)
    bairro = models.CharField(_('Bairro'), max_length=100, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=100, blank=True)
    estado = models.CharField(_('Estado'), max_length=2, blank=True)
    plano_saude = models.CharField(_('Plano de Saúde'), max_length=100, blank=True)

    # Foto de perfil opcional
    foto = models.ImageField(
        _('Foto de perfil'),
        upload_to='usuarios/fotos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

