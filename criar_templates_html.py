import os
from pathlib import Path

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo, garantindo que a pasta exista (Corrigido para evitar FileNotFoundError)."""
    pasta = os.path.dirname(caminho)
    
    # Garante que todas as pastas no caminho existam (e ignora se já existirem)
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    # O arquivo agora pode ser criado sem erro
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ Arquivo criado/atualizado: {caminho}")

def criar_base_templates():
    """Cria os templates base globais (base/, home, dashboard)"""
    
    print("\n📝 Criando templates base globais...")
    
    # 1. templates/base/base.html (Estrutura principal com Bootstrap)
    base_html_content = """{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ACJogos Intranet{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link rel="stylesheet" href="{% static 'css/style.css' %}"> 
</head>
<body class="bg-light">
    <div class="container-fluid">
        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
"""
    criar_arquivo('templates/base/base.html', base_html_content)

    # 2. templates/base/home.html (Página pública)
    home_html_content = """{% extends "base/base.html" %}

{% block title %}Home - {{ titulo }}{% endblock %}

{% block content %}
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
{% endblock %}
"""
    criar_arquivo('templates/base/home.html', home_html_content)

    # 3. templates/base/dashboard.html (Página após login)
    dashboard_html_content = """{% extends "base/base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="row pt-5">
    <div class="col-12">
        <h1 class="mt-5">Olá, {{ user.get_full_name|default:user.username }}!</h1>
        <p class="lead">Bem-vindo ao Dashboard. A funcionalidade de login está pronta!</p>
        <p>Próximo passo: construir o menu de navegação e as interfaces de cada app.</p>
        
        <div class="mt-4">
            <a class="btn btn-info me-2" href="/admin/">Ir para o Admin</a>
            <a class="btn btn-danger" href="{% url 'accounts:logout' %}">Sair</a>
        </div>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/base/dashboard.html', dashboard_html_content)
    
    # 4. templates/base/em_construcao.html (Para apps vazios)
    em_construcao_content = """{% extends "base/base.html" %}

{% block title %}Em Construção{% endblock %}

{% block content %}
<div class="row justify-content-center text-center pt-5">
    <div class="col-md-8">
        <h1 class="mt-5">App '{{ app_name|default:"Esta Página" }}' em Construção</h1>
        <p class="lead">O sistema está estruturalmente pronto, mas a interface desta página ainda não foi desenvolvida.</p>
        <p><a href="{% url 'accounts:home' %}">Voltar para Home</a></p>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/base/em_construcao.html', em_construcao_content)

def criar_auth_templates():
    """Cria os templates de Login, Registro e Recuperação de Senha"""
    
    print("\n📝 Criando templates de Autenticação (Login, Registro, Senha)...")
    
    # 1. accounts/login.html (Tela bonita de Login)
    login_html_content = """{% extends "base/base.html" %}
{% load crispy_forms_tags %}

{% block title %}Login - Intranet{% endblock %}

{% block content %}
<div class="row justify-content-center pt-5">
    <div class="col-md-6 col-lg-4">
        
        <div class="card shadow-lg border-0 rounded-lg mt-5">
            <div class="card-header bg-primary text-white text-center">
                <h3 class="fw-light my-4">Acesso à Intranet</h3>
            </div>
            <div class="card-body">
                
                {% if form.errors %}
                <div class="alert alert-danger" role="alert">
                    Usuário ou senha inválidos. Tente novamente.
                </div>
                {% endif %}

                <form method="post">
                    {% csrf_token %}
                    
                    {{ form|crispy }}
                    
                    <div class="d-flex align-items-center justify-content-between mt-4 mb-0">
                        <a class="small" href="{% url 'password_reset' %}">Esqueceu a senha?</a>
                        <button type="submit" class="btn btn-primary">Entrar</button>
                    </div>
                </form>
            </div>
            <div class="card-footer text-center py-3">
                <div class="small">Não tem conta? <a href="{% url 'accounts:registrar' %}">Criar Conta</a></div>
            </div>
        </div>

    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/accounts/login.html', login_html_content)

    # 2. accounts/registrar.html (Tela bonita de Registro)
    registrar_html_content = """{% extends "base/base.html" %}
{% load crispy_forms_tags %}

{% block title %}Registrar - Intranet{% endblock %}

{% block content %}
<div class="row justify-content-center pt-5">
    <div class="col-md-8 col-lg-6">
        
        <div class="card shadow-lg border-0 rounded-lg mt-5">
            <div class="card-header bg-success text-white text-center">
                <h3 class="fw-light my-4">Criar uma Nova Conta</h3>
            </div>
            <div class="card-body">
                
                <form method="post" novalidate>
                    {% csrf_token %}
                    
                    {{ form|crispy }}
                    
                    <div class="d-grid gap-2 mt-4 mb-0">
                        <button type="submit" class="btn btn-success btn-block">Registrar</button>
                    </div>
                </form>
            </div>
            <div class="card-footer text-center py-3">
                <div class="small">
                    Já tem uma conta? <a href="{% url 'accounts:login' %}">Faça o Login</a>
                </div>
            </div>
        </div>

    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/accounts/registrar.html', registrar_html_content)
    
    # 3. templates/registration/password_reset_form.html (Recuperação de Senha - 1)
    reset_form_content = """{% extends "base/base.html" %}
{% load crispy_forms_tags %}

{% block title %}Redefinir Senha{% endblock %}

{% block content %}
<div class="row justify-content-center pt-5">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow-lg border-0 rounded-lg mt-5">
            <div class="card-header bg-warning text-dark text-center">
                <h3 class="fw-light my-4">Redefinir Senha</h3>
            </div>
            <div class="card-body">
                <p>Insira seu email para receber as instruções de redefinição.</p>
                <form method="post">
                    {% csrf_token %}
                    {{ form|crispy }}
                    <div class="d-grid gap-2 mt-4">
                        <button type="submit" class="btn btn-warning">Enviar email</button>
                    </div>
                </form>
            </div>
            <div class="card-footer text-center py-3">
                <div class="small"><a href="{% url 'accounts:login' %}">Voltar para o Login</a></div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/registration/password_reset_form.html', reset_form_content)
    
    # 4. templates/registration/password_reset_done.html (Recuperação de Senha - 2)
    reset_done_content = """{% extends "base/base.html" %}

{% block title %}Email Enviado{% endblock %}

{% block content %}
<div class="row justify-content-center pt-5 text-center">
    <div class="col-md-6">
        <h1 class="mt-5">Verifique seu Email</h1>
        <p class="lead">Enviamos um email com as instruções para redefinir sua senha.</p>
        <p>Se você não recebeu o email, verifique sua pasta de Spam.</p>
        <p><a href="{% url 'accounts:login' %}" class="btn btn-primary mt-3">Voltar ao Login</a></p>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/registration/password_reset_done.html', reset_done_content)
    
    # 5. templates/registration/password_reset_confirm.html (Recuperação de Senha - 3)
    reset_confirm_content = """{% extends "base/base.html" %}
{% load crispy_forms_tags %}

{% block title %}Nova Senha{% endblock %}

{% block content %}
<div class="row justify-content-center pt-5">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow-lg border-0 rounded-lg mt-5">
            <div class="card-header bg-primary text-white text-center">
                <h3 class="fw-light my-4">Definir Nova Senha</h3>
            </div>
            <div class="card-body">
                {% if validlink %}
                    <p>Crie uma nova senha.</p>
                    <form method="post">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <div class="d-grid gap-2 mt-4">
                            <button type="submit" class="btn btn-primary">Alterar Senha</button>
                        </div>
                    </form>
                {% else %}
                    <div class="alert alert-danger">
                        O link de redefinição expirou ou é inválido.
                    </div>
                    <a href="{% url 'password_reset' %}" class="btn btn-warning">Tentar novamente</a>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/registration/password_reset_confirm.html', reset_confirm_content)
    
    # 6. templates/registration/password_reset_complete.html (Recuperação de Senha - 4)
    reset_complete_content = """{% extends "base/base.html" %}

{% block title %}Senha Alterada{% endblock %}

{% block content %}
<div class="row justify-content-center pt-5 text-center">
    <div class="col-md-6">
        <h1 class="mt-5">Senha Alterada com Sucesso!</h1>
        <p class="lead">Sua senha foi redefinida. Agora você pode fazer o login com a nova senha.</p>
        <p><a href="{% url 'accounts:login' %}" class="btn btn-primary mt-3">Fazer Login</a></p>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/registration/password_reset_complete.html', reset_complete_content)
    
    print("\n✅ Todos os templates de autenticação e base foram criados com sucesso!")


def main():
    print("=" * 70)
    print("🚀 SCRIPT DE AUTOMAÇÃO: CRIAÇÃO DE TODOS OS TEMPLATES HTML")
    print("=" * 70)
    
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django.")
        return

    # 1. Cria os templates base (base/base.html, home.html, dashboard.html)
    criar_base_templates()
        
    # 2. Cria os templates de Autenticação (Login, Registro e Senha)
    criar_auth_templates()
    
    print("\n" + "=" * 70)
    print("✅ TODOS OS TEMPLATES ESSENCIAIS FORAM CRIADOS.")
    print("   O erro 'TemplateDoesNotExist' deve estar resolvido.")
    print("=" * 70)
    print("\n📋 PRÓXIMOS PASSOS (Teste Final):")
    print("   1. Certifique-se de ter criado o Superusuário:")
    print("      python manage.py createsuperuser")
    print("   2. Inicie o servidor (o erro deve desaparecer):")
    print("      python manage.py runserver")
    print("   3. Teste o acesso:")
    print("      - Home: http://127.0.0.1:8000/")
    print("      - Registro: http://127.0.0.1:8000/registrar/")
    print("      - Login: http://127.0.0.1:8000/login/")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()