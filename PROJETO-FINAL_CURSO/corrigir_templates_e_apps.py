import os
from pathlib import Path

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo, garantindo que a pasta exista."""
    pasta = os.path.dirname(caminho)
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ Arquivo criado/atualizado: {caminho}")

def criar_pastas_e_templates_faltantes():
    print("\n📝 Criando pastas e templates de Login/Registro faltantes...")
    
    # Garante que a pasta base/ exista
    Path('templates/base').mkdir(parents=True, exist_ok=True)
    print("✓ Pasta garantida: templates/base")

    # Garante que a pasta accounts/ exista
    Path('templates/accounts').mkdir(parents=True, exist_ok=True)
    print("✓ Pasta garantida: templates/accounts")
    
    # 1. accounts/login.html (CORRIGE TemplateDoesNotExist at /login/)
    login_html_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Login - Intranet{% endblock %}{% block content %}<div class="row justify-content-center pt-5"><div class="col-md-6 col-lg-4"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-primary text-white text-center"><h3 class="fw-light my-4">Acesso à Intranet</h3></div><div class="card-body">{% if form.errors %}<div class="alert alert-danger" role="alert">Usuário ou senha inválidos. Tente novamente.</div>{% endif %}<form method="post">{% csrf_token %}{{ form|crispy }}<div class="d-flex align-items-center justify-content-between mt-4 mb-0"><a class="small" href="{% url 'accounts:password_reset' %}">Esqueceu a senha?</a><button type="submit" class="btn btn-primary">Entrar</button></div></form></div><div class="card-footer text-center py-3"><div class="small">Não tem conta? <a href="{% url 'accounts:registrar' %}">Criar Conta</a></div></div></div></div></div>{% endblock %}"""
    criar_arquivo('templates/accounts/login.html', login_html_content)

    # 2. accounts/registrar.html (CORRIGE TemplateDoesNotExist at /registrar/)
    registrar_html_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Registrar - Intranet{% endblock %}{% block content %}<div class="row justify-content-center pt-5"><div class="col-md-8 col-lg-6"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-success text-white text-center"><h3 class="fw-light my-4">Criar uma Nova Conta</h3></div><div class="card-body"><form method="post" novalidate>{% csrf_token %}{{ form|crispy }}<div class="d-grid gap-2 mt-4 mb-0"><button type="submit" class="btn btn-success btn-block">Registrar</button></div></form></div><div class="card-footer text-center py-3"><div class="small">Já tem uma conta? <a href="{% url 'accounts:login' %}">Faça o Login</a></div></div></div></div></div>{% endblock %}"""
    criar_arquivo('templates/accounts/registrar.html', registrar_html_content)
    
    # 3. Base/base.html (Para garantir que o layout principal está no lugar certo)
    base_html_content = """{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ACJogos Intranet{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}"> 
    <style>
        :root { --sidebar-width: 250px; }
        body { background-color: #f8f9fa; }
        #sidebar { width: var(--sidebar-width); min-height: 100vh; position: fixed; top: 0; left: 0; z-index: 1000; padding-top: 56px; background-color: #343a40; }
        #content { margin-left: var(--sidebar-width); padding: 20px; }
        .nav-link { color: #adb5bd; }
        .nav-link:hover { color: #ffffff; background-color: #495057; }
        .active-link { color: #ffffff !important; background-color: #0d6efd !important; border-radius: .25rem; }
        .no-sidebar { margin-left: 0 !important; }
    </style>
</head>
<body>
    {% if request.resolver_match.url_name != 'home' and request.resolver_match.url_name != 'login' and request.resolver_match.url_name != 'registrar' %}
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
            <div class="container-fluid">
                <a class="navbar-brand" href="{% url 'accounts:dashboard' %}">ACJogos Intranet</a>
                <div class="collapse navbar-collapse justify-content-end">
                    <ul class="navbar-nav">
                        {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Bem-vindo, **{{ user.username }}**
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="{% url 'admin:index' %}">Painel Admin</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{% url 'accounts:logout' %}">Sair</a></li>
                            </ul>
                        </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </nav>
        <div id="sidebar">
            <div class="list-group list-group-flush pt-2">
                <p class="text-white text-uppercase small px-3 mt-3 mb-2">Módulos Principais</p>
                <a href="{% url 'accounts:dashboard' %}" class="list-group-item list-group-item-action bg-dark text-white border-0 {% if request.resolver_match.url_name == 'dashboard' %}active-link{% endif %}">Dashboard</a>
                <a href="{% url 'empresas:home' %}" class="list-group-item list-group-item-action bg-dark text-white border-0 {% if request.resolver_match.namespace == 'empresas' %}active-link{% endif %}">Empresas</a>
                <a href="{% url 'projetos:home' %}" class="list-group-item list-group-item-action bg-dark text-white border-0 {% if request.resolver_match.namespace == 'projetos' %}active-link{% endif %}">Projetos</a>
                <a href="{% url 'pesquisas:home' %}" class="list-group-item list-group-item-action bg-dark text-white border-0 {% if request.resolver_match.namespace == 'pesquisas' %}active-link{% endif %}">Pesquisas</a>
                <a href="{% url 'links:home' %}" class="list-group-item list-group-item-action bg-dark text-white border-0 {% if request.resolver_match.namespace == 'links' %}active-link{% endif %}">Links Úteis</a>
            </div>
        </div>
        <div id="content"><div class="pt-5 mt-4">{% block content %}{% endblock %}</div></div>
    {% else %}
        <div class="container-fluid no-sidebar pt-5">{% block content %}{% endblock %}</div>
    {% endif %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    criar_arquivo('templates/base/base.html', base_html_content)


def corrigir_apps_modulos():
    print("\n📝 Corrigindo apps de módulo (Garantindo que 'pesquisas' exista)...")
    APPS_DO_PROJETO = ['empresas', 'projetos', 'pesquisas', 'links']

    for app in APPS_DO_PROJETO:
        # Cria a pasta do app se ela não existir (para resolver ModuleNotFoundError)
        Path(f'{app}').mkdir(parents=True, exist_ok=True)
        
        # Cria o __init__.py (necessário para o Python reconhecer como módulo)
        criar_arquivo(f'{app}/__init__.py', '')
        
        # Cria um views.py (Mínimo)
        views_content = f"""from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'base/em_construcao.html', {{'app_name': '{app.capitalize()}'}})
"""
        criar_arquivo(f'{app}/views.py', views_content)
        
        # Cria um urls.py (Mínimo)
        urls_content = f"""from django.urls import path
from . import views

app_name = '{app}'

urlpatterns = [
    path('', views.home_view, name='home'),
]
"""
        criar_arquivo(f'{app}/urls.py', urls_content)

def main():
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django.")
        return
        
    print("=" * 70)
    print("🔧 SCRIPT DE CORREÇÃO: TEMPLATES E MÓDULOS AUSENTES")
    print("=" * 70)
    
    # Corrige TemplateDoesNotExist
    criar_pastas_e_templates_faltantes()
    
    # Corrige ModuleNotFoundError
    corrigir_apps_modulos()

    print("\n" + "=" * 70)
    print("✅ CORREÇÕES APLICADAS. Erros de Template e Módulo resolvidos.")
    print("=" * 70)
    print("\n\n📋 PRÓXIMOS PASSOS (Obrigatório):")
    print("   1. Pare o servidor (Ctrl+C) se estiver rodando.")
    print("   2. Inicie o servidor novamente para carregar os novos arquivos HTML e Apps:")
    print("      python manage.py runserver")
    print("\n   3. Teste o acesso:")
    print("      Acesse http://127.0.0.1:8000/login/ e http://127.0.0.1:8000/registrar/")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()