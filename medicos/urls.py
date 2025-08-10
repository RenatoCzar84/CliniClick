from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicos_especialidades, name='medicos_especialidades'),
]

