from django.contrib import admin
from .models import Medico, Paciente, Consulta

admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Consulta)