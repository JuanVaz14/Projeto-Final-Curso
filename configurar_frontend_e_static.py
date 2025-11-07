import os
from pathlib import Path

# Lista de todos os apps que precisam de views básicas
APPS_DO_PROJETO = ['accounts', 'empresas', 'projetos', 'pesquisas', 'links']

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo, garantindo que a pasta exista."""
    pasta = os.path.dirname(caminho)
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ Arquivo criado/atualizado: {caminho}")

def criar_pastas_static():
    """Cria as pastas básicas para arquivos estáticos."""
    print("\n📝 Criando estrutura de pastas estáticas...")
    pastas = [
        'static/css', 
        'static/js', 
        'static/img',
    ]
    
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"✓ Pasta criada: {pasta}")
        
    # Cria o arquivo CSS inicial
    css_content = """/* * Arquivo: style.css
 * Este arquivo foi criado automaticamente. 
 * Use-o para adicionar estilos customizados que sobrescrevem o Bootstrap.
 * * Exemplo:
 * body {
 * font-family: 'Arial', sans-serif;
 * }
 */
 
/* Você pode adicionar estilos aqui para manter o código limpo */
"""
    criar_arquivo('static/css/style.css', css_content)

def atualizar_views_placeholders():
    """Garante que todas as views dos apps secundários apontem para o template de 'Em Construção'."""
    print("\n📝 Atualizando views.py para usar o template 'Em Construção'...")
    
    for app in APPS_DO_PROJETO:
        if app == 'accounts':
            # Ignora accounts, pois ele tem views específicas (login, dashboard)
            continue
            
        app_views_content = f"""from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def {app}_home(request):
    # Esta view usa o template 'em_construcao.html' que herda o layout bonito.
    # Quando for desenvolver, mude o render para '{app}/{app}_home.html'
    return render(request, 'base/em_construcao.html', {{'app_name': '{app}'}})

"""
        criar_arquivo(f'{app}/views.py', app_views_content)
        
    # Garante que as views de accounts (dashboard e home) também usam o layout bonito
    accounts_views_content = f"""from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from .forms import UsuarioCreationForm 


# Home pública
def home_view(request):
    return render(request, 'base/home.html', {{'titulo': 'Bem-vindo à Intranet ACJogos-RJ'}})

# Dashboard (acesso após login)
@login_required
def dashboard_view(request):
    # Usa o novo template dashboard.html com o layout side-bar
    return render(request, 'base/dashboard.html', {{'titulo': 'Dashboard'}})


# View de Registro
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('accounts:dashboard')
    else:
        form = UsuarioCreationForm()
    
    context = {{'form': form, 'titulo': 'Criar Conta'}}
    return render(request, 'accounts/registrar.html', context)
"""
    criar_arquivo(f'accounts/views.py', accounts_views_content)

def main():
    print("=" * 70)
    print("🚀 SCRIPT DE AUTOMAÇÃO: CONFIGURAÇÃO GRÁFICA E STATIC FILES")
    print("=" * 70)
    
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django.")
        return

    # 1. Cria a estrutura de pastas estáticas (CSS, JS, IMG)
    criar_pastas_static()
        
    # 2. Atualiza todas as views para garantir que o layout bonito seja usado
    atualizar_views_placeholders()
    
    print("\n" + "=" * 70)
    print("✅ CONFIGURAÇÃO GRÁFICA BASE CONCLUÍDA.")
    print("   Todos os apps carregam o layout de Dashboard/Sidebar.")
    print("=" * 70)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("   1. Inicie o servidor (se não estiver rodando):")
    print("      python manage.py runserver")
    print("   2. Faça o login em http://127.0.0.1:8000/login/")
    print("   3. Teste os links da Sidebar (Empresas, Projetos etc.) - todos carregarão a página 'Em Construção' com a barra lateral!")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()