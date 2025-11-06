import os
from pathlib import Path

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo com o conteúdo fornecido"""
    pasta = os.path.dirname(caminho)
    # Garante que a pasta existe antes de tentar escrever o arquivo
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ Arquivo criado/atualizado: {caminho}")

def criar_views_para_apps(apps):
    """Cria arquivos views.py básicos para os apps e o views.py principal para 'accounts'"""
    
    print("\n📝 Criando/Atualizando views.py...")
    
    # 1. accounts/views.py (com as views de Home e Dashboard para resolver o 404)
    accounts_views_content = """from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Home pública (acesso em 127.0.0.1:8000/)
def home_view(request):
    return render(request, 'base/home.html', {'titulo': 'Bem-vindo à Intranet ACJogos-RJ'})

# Dashboard (acesso após login)
@login_required
def dashboard_view(request):
    return render(request, 'base/dashboard.html', {'titulo': 'Dashboard'})

"""
    criar_arquivo('accounts/views.py', accounts_views_content)
    
    # 2. views.py básico para os demais apps
    for app in apps:
        if app != 'accounts':
            app_views_content = f"""from django.shortcuts import render

def {app}_home(request):
    # Exemplo de view simples para o app {app}
    return render(request, 'base/em_construcao.html', {{'app_name': '{app}'}})
"""
            criar_arquivo(f'{app}/views.py', app_views_content)

def criar_templates_minimos():
    """Cria os templates mínimos para evitar erros de TemplateDoesNotExist"""
    print("\n📝 Criando templates mínimos em /templates/base/...")
    
    # Template Base: Home pública
    home_html_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ titulo }}</title>
</head>
<body>
    <h1>Bem-vindo à Intranet ACJogos-RJ!</h1>
    <p>O servidor está funcionando!</p>
    <p>Acesse o <a href="/admin/">Admin</a> ou o <a href="/login/">Login</a>.</p>
</body>
</html>
"""
    criar_arquivo('templates/base/home.html', home_html_content)

    # Template Base: Dashboard (página inicial após login)
    dashboard_html_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ titulo }}</title>
</head>
<body>
    <h1>Dashboard</h1>
    <p>Você acessou o Dashboard após a correção estrutural. O servidor está funcionando!</p>
    <p>O próximo passo é construir a interface de usuário!</p>
    <p><a href="/admin/">Ir para o Admin</a></p>
    <p><a href="/logout/">Sair</a></p>
</body>
</html>
"""
    criar_arquivo('templates/base/dashboard.html', dashboard_html_content)
    
    # Template Base: Em Construção (para os outros apps)
    em_construcao_content = """<!DOCTYPE html>
<html>
<head>
    <title>Em Construção</title>
</head>
<body>
    <h1>Página do App '{{ app_name }}' em Construção</h1>
    <p>Este app está estruturalmente pronto, mas a página ainda não foi desenvolvida.</p>
    <p><a href="/">Voltar para Home</a></p>
</body>
</html>
"""
    criar_arquivo('templates/base/em_construcao.html', em_construcao_content)

def atualizar_urls_apps(apps):
    """Atualiza o urls.py de cada app para mapear a view recém-criada (resolve o 404)"""
    print("\n📝 Atualizando/Criando arquivos urls.py para mapeamento de views...")
    
    # 1. accounts/urls.py (o mais crítico)
    accounts_urls_content = """from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # views é o accounts/views.py

app_name = 'accounts'

urlpatterns = [
    # URLs de Autenticação padrão do Django
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # ROTA HOME/DASHBOARD
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('', views.home_view, name='home'), # Mapeia a URL vazia (/) para a Home pública
]
"""
    criar_arquivo('accounts/urls.py', accounts_urls_content)
    
    # 2. Atualiza os demais apps para a view base
    for app in apps:
        if app != 'accounts':
            app_urls_content = f"""from django.urls import path
from . import views

# Define o namespace do app
app_name = '{app}'

urlpatterns = [
    path('', views.{app}_home, name='home'),
]
"""
            criar_arquivo(f'{app}/urls.py', app_urls_content)


def main():
    print("=" * 60)
    print("🚀 SCRIPT DE AUTOMAÇÃO E CORREÇÃO FINAL (VIEWS e TEMPLATES)")
    print("=" * 60)
    
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django.")
        return

    # Lista de todos os apps
    apps_necessarios = ['accounts', 'empresas', 'projetos', 'pesquisas', 'links']
    
    # 1. Cria ou sobrescreve os arquivos views.py
    criar_views_para_apps(apps_necessarios)
        
    # 2. Cria os templates HTML mínimos
    criar_templates_minimos()
    
    # 3. Atualiza os urls.py para mapear as views (resolvendo o 404)
    atualizar_urls_apps(apps_necessarios)
    
    print("\n" + "=" * 60)
    print("✅ ESTRUTURA LÓGICA PRONTA! O SERVIDOR DEVE INICIAR SEM 404.")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("   1. Crie um superusuário (necessário para o admin):")
    print("      python manage.py createsuperuser")
    print("   2. Inicie o servidor (o 404 deve sumir):")
    print("      python manage.py runserver")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()