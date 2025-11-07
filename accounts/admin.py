from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'ativo')
    list_filter = ('is_staff', 'is_superuser', 'tipo_usuario', 'ativo')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'cpf')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações ACJogos-RJ', {
            'fields': ('tipo_usuario', 'nome_social', 'cpf', 'telefone', 'nick_discord',
                      'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 
                      'estado', 'data_associacao', 'ativo', 'foto_perfil')
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)
