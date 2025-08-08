from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    # O que aparece na listagem
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'cpf', 'first_name', 'last_name')

    # Campos ao editar um usuário existente
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Pessoais', {
            'fields': ('cep', 'logradouro', 'bairro', 'cidade', 'estado',
                       'telefone', 'cpf', 'data_nascimento', 'plano_saude')
        }),
    )

    # Campos ao criar um usuário via admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados Pessoais', {
            'classes': ('wide',),
            'fields': ('cep', 'logradouro', 'bairro', 'cidade', 'estado',
                       'telefone', 'cpf', 'data_nascimento', 'plano_saude'),
        }),
    )
