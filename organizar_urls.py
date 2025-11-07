import os

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo com o conteúdo fornecido"""
    pasta = os.path.dirname(caminho)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)
        
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"✓ Arquivo criado/atualizado: {caminho}")
    except Exception as e:
        print(f"❌ Erro ao criar arquivo {caminho}: {e}")

def criar_urls_app(app_name):
    """Cria o arquivo urls.py básico para um aplicativo"""
    caminho = os.path.join(app_name, 'urls.py')
    conteudo = f"""from django.urls import path
from . import views

# Define o namespace do app
app_name = '{app_name}'

urlpatterns = [
    # Adicione suas rotas aqui, ex:
    # path('', views.home_view, name='home'),
]
"""
    criar_arquivo(caminho, conteudo)

def criar_urls_principal(apps):
    """Cria o arquivo urls.py principal do projeto, incluindo todos os apps"""
    caminho = os.path.join('acjogos_intranet', 'urls.py')
    includes = "\n".join([f"    path('{app}/', include('{app}.urls'))," for app in apps if app != 'accounts'])
    
    conteudo = f"""# Arquivo urls.py principal do projeto

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs do Django Admin
    path('admin/', admin.site.urls),
    
    # URLS do app accounts (usando o path vazio para ser a base do login/dashboard)
    path('', include('accounts.urls')),
    
    # Inclusão de todos os outros aplicativos
{includes}
]

# Configuração para servir arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    # Garante que o arquivo é criado na pasta de configuração do projeto
    criar_arquivo(caminho, conteudo)

def main():
    print("=" * 60)
    print("🔗 ORGANIZANDO E CRIANDO ARQUIVOS DE URLS FALTANTES")
    print("=" * 60)
    
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django.")
        return

    # Lista de todos os apps
    apps_necessarios = ['accounts', 'empresas', 'projetos', 'pesquisas', 'links']
    
    # 1. Cria os urls.py para cada app
    for app in apps_necessarios:
        criar_urls_app(app)
        
    # 2. Cria o urls.py principal, incluindo todos os apps
    criar_urls_principal(apps_necessarios)
    
    print("\n" + "=" * 60)
    print("✅ ESTRUTURA DE URLS CORRIGIDA!")
    print("=" * 60)
    print("\n📋 PRÓXIMO PASSO:")
    print("   python manage.py runserver")

if __name__ == '__main__':
    main()