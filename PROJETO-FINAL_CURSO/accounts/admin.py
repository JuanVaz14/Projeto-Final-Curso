from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario  # CORREÇÃO CRÍTICA: Importação relativa correta

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_usuario', 'ativo')
    list_editable = ('ativo',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'tipo_usuario', 'ativo')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'cpf')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Customizadas ACJogos-RJ', 
         {'fields': ('tipo_usuario', 'nome_social', 'cpf', 'telefone', 'nick_discord', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'data_associacao', 'ativo', 'foto_perfil')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Customizadas ACJogos-RJ', 
         {'fields': ('tipo_usuario', 'nome_social', 'cpf', 'telefone', 'nick_discord', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'data_associacao', 'ativo', 'foto_perfil')}),
    )

try:
    admin.site.unregister(Usuario)
except admin.sites.NotRegistered:
    pass

admin.site.register(Usuario, UsuarioAdmin)
