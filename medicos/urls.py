# medicos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.medicos_e_especialidades, name="medicos_e_especialidades"),
]