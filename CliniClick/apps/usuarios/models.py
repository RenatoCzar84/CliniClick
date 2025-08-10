from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    cep = models.CharField(max_length=10, blank=True)
    logradouro = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    plano_saude = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
