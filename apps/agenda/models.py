from django.db import models
from django.db import models
from django.conf import settings

class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=120)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, related_name="medicos")
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["especialidade__nome", "nome"]
        unique_together = ("nome", "especialidade")

    def __str__(self):
        return f"{self.nome} ({self.especialidade.nome})"

class ExameTipo(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    TIPO_CONSULTA = "consulta"
    TIPO_EXAME = "exame"
    TIPO_CHOICES = [
        (TIPO_CONSULTA, "Consulta"),
        (TIPO_EXAME, "Exame"),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="agendamentos")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    # Para consulta
    especialidade = models.ForeignKey(Especialidade, null=True, blank=True, on_delete=models.PROTECT)
    medico = models.ForeignKey(Medico, null=True, blank=True, on_delete=models.PROTECT)

    # Para exame
    exame_tipo = models.ForeignKey(ExameTipo, null=True, blank=True, on_delete=models.PROTECT)

    data_hora = models.DateTimeField()
    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["data_hora"]

    def __str__(self):
        if self.tipo == self.TIPO_CONSULTA:
            alvo = self.medico or self.especialidade
        else:
            alvo = self.exame_tipo
        return f"{self.get_tipo_display()} - {alvo} em {self.data_hora:%d/%m/%Y %H:%M}"
# Create your models here.
