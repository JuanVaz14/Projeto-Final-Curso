import os
from pathlib import Path

# --- Funções de Utilidade ---

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo, garantindo que a pasta exista."""
    pasta = os.path.dirname(caminho)
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ Arquivo corrigido/atualizado: {caminho}")

def corrigir_templates_completos():
    print("\n📝 Corrigindo todos os Templates (Renomeando 'block content' para 'main_content')...")
    
    # 1. Base/base.html (CORRIGIDO: Usa 'main_content' e mantém a estrutura condicional)
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
        #sidebar {
            width: var(--sidebar-width);
            min-height: 100vh;
            position: fixed; top: 0; left: 0; z-index: 1000;
            padding-top: 56px; background-color: #343a40;
        }
        #content {
            margin-left: var(--sidebar-width);
            padding: 20px;
        }
        .nav-link { color: #adb5bd; }
        .nav-link:hover { color: #ffffff; background-color: #495057; }
        .active-link { color: #ffffff !important; background-color: #0d6efd !important; border-radius: .25rem; }
        /* Ajuste para o login/home sem sidebar */
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
        
        <div id="content">
            <div class="pt-5 mt-4"> 
                {% block main_content %}{% endblock %}
            </div>
        </div>
    {% else %}
        <div class="container-fluid no-sidebar pt-5">
            {% block main_content %}{% endblock %}
        </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    criar_arquivo('templates/base/base.html', base_html_content)

    # 2. Base/home.html (Usando main_content)
    home_html_content = """{% extends "base/base.html" %}
{% block title %}Home - {{ titulo }}{% endblock %}
{% block main_content %}
<div class="row justify-content-center text-center pt-5">
    <div class="col-md-8">
        <h1 class="display-4 mt-5">Bem-vindo à Intranet ACJogos-RJ!</h1>
        <p class="lead">O servidor está funcionando e a estrutura está pronta.</p>
        <hr class="my-4">
        <p>Acesse as áreas do sistema:</p>
        <p class="mt-4">
            <a class="btn btn-primary btn-lg me-2" href="{% url 'accounts:login' %}" role="button">Fazer Login</a>
            <a class="btn btn-success btn-lg me-2" href="{% url 'accounts:registrar' %}" role="button">Criar Conta</a>
            <a class="btn btn-secondary btn-lg" href="/admin/" role="button">Admin (Apenas Superusuários)</a>
        </p>
    </div>
</div>
{% endblock main_content %}
"""
    criar_arquivo('templates/base/home.html', home_html_content)
    
    # 3. Base/dashboard.html (Usando main_content)
    dashboard_html_content = """{% extends "base/base.html" %}

{% block title %}Dashboard{% endblock %}

{% block main_content %}
<h1 class="mb-4">Dashboard Principal</h1>
<p class="lead">Visão geral do sistema. Olá, **{{ user.get_full_name|default:user.username }}**!</p>

<div class="row">
    <div class="col-xl-3 col-md-6 mb-4"><div class="card border-left-primary shadow h-100 py-2"><div class="card-body"><div class="row no-gutters align-items-center"><div class="col me-2"><div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Empresas Cadastradas</div><div class="h5 mb-0 font-weight-bold text-gray-800">120</div></div></div></div></div><a href="{% url 'empresas:home' %}" class="card-footer bg-white text-primary small">Ver Detalhes &rarr;</a></div>
    <div class="col-xl-3 col-md-6 mb-4"><div class="card border-left-success shadow h-100 py-2"><div class="card-body"><div class="row no-gutters align-items-center"><div class="col me-2"><div class="text-xs font-weight-bold text-success text-uppercase mb-1">Projetos Ativos</div><div class="h5 mb-0 font-weight-bold text-gray-800">45</div></div></div></div></div><a href="{% url 'projetos:home' %}" class="card-footer bg-white text-success small">Ver Projetos &rarr;</a></div>
    <div class="col-xl-3 col-md-6 mb-4"><div class="card border-left-warning shadow h-100 py-2"><div class="card-body"><div class="row no-gutters align-items-center"><div class="col me-2"><div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Pesquisas Pendentes</div><div class="h5 mb-0 font-weight-bold text-gray-800">5</div></div></div></div></div><a href="{% url 'pesquisas:home' %}" class="card-footer bg-white text-warning small">Responder &rarr;</a></div>
    <div class="col-xl-3 col-md-6 mb-4"><div class="card border-left-info shadow h-100 py-2"><div class="card-body"><div class="row no-gutters align-items-center"><div class="col me-2"><div class="text-xs font-weight-bold text-info text-uppercase mb-1">Seu Perfil</div><div class="h5 mb-0 font-weight-bold text-gray-800">{{ user.tipo_usuario|default:"Não Definido" }}</div></div></div></div></div></div>
</div>

<hr>
<div class="alert alert-info">
    Clique nos links na barra lateral (Sidebar) para navegar para as páginas "Em Construção".
</div>
{% endblock main_content %}
"""
    criar_arquivo('templates/base/dashboard.html', dashboard_html_content)
    
    # 4. Base/em_construcao.html (Usando main_content)
    em_construcao_content = """{% extends "base/base.html" %}

{% block title %}Em Construção{% endblock %}

{% block main_content %}
<div class="row justify-content-center text-center pt-5">
    <div class="col-md-10">
        <h1 class="mt-5 display-4">App '{{ app_name|default:"Esta Página" }}' em Construção</h1>
        <p class="lead">O layout gráfico está funcionando! Agora, vamos desenvolver esta página.</p>
        <p><a href="{% url 'accounts:dashboard' %}" class="btn btn-secondary mt-3">Voltar ao Dashboard</a></p>
    </div>
</div>
{% endblock main_content %}
"""
    criar_arquivo('templates/base/em_construcao.html', em_construcao_content)
    
    # 5. Templates de Autenticação (Usando main_content)
    
    # templates/accounts/login.html
    login_html_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Login - Intranet{% endblock %}{% block main_content %}<div class="row justify-content-center pt-5"><div class="col-md-6 col-lg-4"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-primary text-white text-center"><h3 class="fw-light my-4">Acesso à Intranet</h3></div><div class="card-body">{% if form.errors %}<div class="alert alert-danger" role="alert">Usuário ou senha inválidos. Tente novamente.</div>{% endif %}<form method="post">{% csrf_token %}{{ form|crispy }}<div class="d-flex align-items-center justify-content-between mt-4 mb-0"><a class="small" href="{% url 'accounts:password_reset' %}">Esqueceu a senha?</a><button type="submit" class="btn btn-primary">Entrar</button></div></form></div><div class="card-footer text-center py-3"><div class="small">Não tem conta? <a href="{% url 'accounts:registrar' %}">Criar Conta</a></div></div></div></div></div>{% endblock main_content %}"""
    criar_arquivo('templates/accounts/login.html', login_html_content)

    # templates/accounts/registrar.html
    registrar_html_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Registrar - Intranet{% endblock %}{% block main_content %}<div class="row justify-content-center pt-5"><div class="col-md-8 col-lg-6"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-success text-white text-center"><h3 class="fw-light my-4">Criar uma Nova Conta</h3></div><div class="card-body"><form method="post" novalidate>{% csrf_token %}{{ form|crispy }}<div class="d-grid gap-2 mt-4 mb-0"><button type="submit" class="btn btn-success btn-block">Registrar</button></div></form></div><div class="card-footer text-center py-3"><div class="small">Já tem uma conta? <a href="{% url 'accounts:login' %}">Faça o Login</a></div></div></div></div></div>{% endblock main_content %}"""
    criar_arquivo('templates/accounts/registrar.html', registrar_html_content)
    
    # templates/registration/*.html (Password Reset)
    reset_form_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Redefinir Senha{% endblock %}{% block main_content %}<div class="row justify-content-center pt-5"><div class="col-md-6 col-lg-4"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-warning text-dark text-center"><h3 class="fw-light my-4">Redefinir Senha</h3></div><div class="card-body"><p>Insira seu email para receber as instruções de redefinição.</p><form method="post">{% csrf_token %}{{ form|crispy }}<div class="d-grid gap-2 mt-4"><button type="submit" class="btn btn-warning">Enviar email</button></div></form></div><div class="card-footer text-center py-3"><div class="small"><a href="{% url 'accounts:login' %}">Voltar para o Login</a></div></div></div></div></div>{% endblock main_content %}"""
    criar_arquivo('templates/registration/password_reset_form.html', reset_form_content)
    
    reset_done_content = """{% extends "base/base.html" %}{% block title %}Email Enviado{% endblock %}{% block main_content %}<div class="row justify-content-center pt-5 text-center"><div class="col-md-6"><h1 class="mt-5">Verifique seu Email</h1><p class="lead">Enviamos um email com as instruções para redefinir sua senha.</p><p><a href="{% url 'accounts:login' %}" class="btn btn-primary mt-3">Voltar ao Login</a></p></div></div>{% endblock main_content %}"""
    criar_arquivo('templates/registration/password_reset_done.html', reset_done_content)
    
    reset_confirm_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Nova Senha{% endblock %}{% block main_content %}<div class="row justify-content-center pt-5"><div class="col-md-6 col-lg-4"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-primary text-white text-center"><h3 class="fw-light my-4">Definir Nova Senha</h3></div><div class="card-body">{% if validlink %}<p>Crie uma nova senha.</p><form method="post">{% csrf_token %}{{ form|crispy }}<div class="d-grid gap-2 mt-4"><button type="submit" class="btn btn-primary">Alterar Senha</button></div></form>{% else %}<div class="alert alert-danger">O link de redefinição expirou ou é inválido.</div><a href="{% url 'accounts:password_reset' %}" class="btn btn-warning">Tentar novamente</a>{% endif %}</div></div></div></div>{% endblock main_content %}"""
    criar_arquivo('templates/registration/password_reset_confirm.html', reset_confirm_content)
    
    reset_complete_content = """{% extends "base/base.html" %}{% block title %}Senha Alterada{% endblock %}{% block main_content %}<div class="row justify-content-center pt-5 text-center"><div class="col-md-6"><h1 class="mt-5">Senha Alterada com Sucesso!</h1><p class="lead">Sua senha foi redefinida. Agora você pode fazer o login com a nova senha.</p><p><a href="{% url 'accounts:login' %}" class="btn btn-primary mt-3">Fazer Login</a></p></div></div>{% endblock main_content %}"""
    criar_arquivo('templates/registration/password_reset_complete.html', reset_complete_content)

def main():
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django.")
        return
        
    print("=" * 70)
    print("🔧 SCRIPT DE CORREÇÃO FINAL: TemplateSyntaxError")
    print("======================================================================")
    
    corrigir_templates_completos()

    print("\n" + "=" * 70)
    print("✅ CORREÇÃO APLICADA. O 'block content' duplicado foi renomeado para 'main_content' em todos os arquivos.")
    print("======================================================================")
    print("\n\n📋 PRÓXIMOS PASSOS (Obrigatório):")
    print("   1. **Pare o servidor** (Ctrl+C) se estiver rodando.")
    print("   2. **Inicie o servidor novamente** para carregar os templates corrigidos:")
    print("      python manage.py runserver")
    print("\n   3. Teste o acesso. A Home (`/`), Login (`/login/`) e Dashboard (`/dashboard/`) devem funcionar agora!")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()