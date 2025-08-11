from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_paciente, name='registro_paciente'),
    path('consultas/', views.lista_consultas, name='lista_consultas'),
    path('consulta/<int:consulta_id>/', views.detalhe_consulta, name='detalhe_consulta'),
]