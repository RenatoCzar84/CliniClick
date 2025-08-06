from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

