from django.urls import path
from . import views

app_name = "agenda"

urlpatterns = [
    path("consultas/novo/", views.agendar_consulta, name="agendar_consulta"),
    path("exames/novo/", views.agendar_exame, name="agendar_exame"),
    path("meus-agendamentos/", views.listar_agendamentos, name="listar_agendamentos"),
    path("agendamentos/<int:pk>/editar/", views.editar_agendamento, name="editar_agendamento"),
    path("agendamentos/<int:pk>/excluir/", views.excluir_agendamento, name="excluir_agendamento"),
    path("medicos-por-especialidade/<int:especialidade_id>/", views.medicos_por_especialidade, name="medicos_por_especialidade"),
]