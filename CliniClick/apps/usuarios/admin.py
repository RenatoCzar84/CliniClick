from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Dados adicionais', {
            'fields': (
                'cpf', 'telefone', 'data_nascimento',
                'cep', 'logradouro', 'bairro', 'cidade', 'estado',
                'plano_saude', 'foto',
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados adicionais', {
            'classes': ('wide',),
            'fields': ('cpf', 'telefone', 'data_nascimento'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'cpf')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cpf')

