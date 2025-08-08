
from django.db import models

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    crm = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Dr(a). {self.nome} - {self.especialidade}"

class Consulta(models.Model):
    paciente = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    data_hora = models.DateTimeField()
    especialidade_desejada = models.CharField(max_length=100)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    motivo = models.TextField()

    def __str__(self):
        return f"Consulta de {self.paciente} com {self.medico.nome}"