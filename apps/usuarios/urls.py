from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),  # opcional
]
