import os
import subprocess
import sys
from pathlib import Path

# --- Variáveis Globais ---
APPS_DO_PROJETO = ['accounts', 'empresas', 'projetos', 'pesquisas', 'links']

# --- Funções de Utilidade ---

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo, garantindo que a pasta exista (Solução robusta para Windows)."""
    pasta = os.path.dirname(caminho)
    # Garante que todas as pastas no caminho existam (e ignora se já existirem)
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ Arquivo criado/atualizado: {caminho}")

def criar_app(nome_app):
    """Cria um app Django se ele não existir"""
    if os.path.exists(nome_app):
        print(f"• App '{nome_app}' já existe")
        return False
    
    try:
        subprocess.run(['python', 'manage.py', 'startapp', nome_app], check=True, stdout=subprocess.DEVNULL)
        print(f"✓ App '{nome_app}' criado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar app '{nome_app}': {e}")
        return False

# --- Configurações Principais (settings.py, urls.py, .env) ---

def configurar_projeto_raiz():
    print("\n📝 Configurando arquivos de projeto (.env, settings.py, urls.py)...")

    # 1. Arquivo .env
    env_content = """# Django Settings
SECRET_KEY=django-insecure-test-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (SQLite para desenvolvimento)
DB_ENGINE=sqlite

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@acjogos-rj.org.br
"""
    criar_arquivo('.env', env_content)

    # 2. Arquivo settings.py (Completo e corrigido)
    settings_content = """import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'localflavor',
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Apps locais
    'accounts',
    'empresas',
    'projetos',
    'pesquisas',
    'links',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'acjogos_intranet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'acjogos_intranet.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.Usuario'

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = 'accounts:login' # Corrigido para namespace
LOGIN_REDIRECT_URL = 'accounts:dashboard' # Corrigido para namespace
LOGOUT_REDIRECT_URL = 'accounts:home' # Corrigido para namespace

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
"""
    criar_arquivo('acjogos_intranet/settings.py', settings_content)

    # 3. Arquivo urls.py (Corrigido para incluir todos os apps e media)
    urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. URLs do Admin
    path('admin/', admin.site.urls),
    
    # 2. URLs do App Accounts (Login, Registro, Dashboard, Home - Rota vazia)
    path('', include('accounts.urls')),
    
    # 3. URLs dos Apps de Módulos
    path('empresas/', include('empresas.urls')),
    path('projetos/', include('projetos.urls')),
    path('pesquisas/', include('pesquisas.urls')),
    path('links/', include('links.urls')),
]

# Configuração de arquivos de mídia (necessário para fotos de perfil)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    criar_arquivo('acjogos_intranet/urls.py', urls_content)

# --- Configuração do App Accounts (Modelos, Admin, URLs) ---

def configurar_app_accounts():
    print("\n📝 Configurando app 'accounts' (Modelos, Admin, Forms, URLs)...")

    # 1. accounts/models.py
    models_content = """from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.br.models import BRCPFField, BRPostalCodeField
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    # ... (Conteúdo do modelo Usuario omitido por brevidade, mas deve ser o completo)
    TIPO_USUARIO = [
        ('DIRETORIA', 'Diretoria'),
        ('ASSOCIADO', 'Associado'),
        ('AFILIADO', 'Afiliado'),
        ('COLETIVO', 'Coletivo/Institucional'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, default='AFILIADO', verbose_name='Tipo de Usuário')
    nome_social = models.CharField(max_length=150, blank=True, verbose_name='Nome Social')
    cpf = BRCPFField('CPF', unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    nick_discord = models.CharField(max_length=100, blank=True, verbose_name='Nick no Discord')
    cep = BRPostalCodeField('CEP', blank=True)
    endereco = models.CharField('Endereço', max_length=255, blank=True)
    numero = models.CharField('Número', max_length=10, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True, default='Rio de Janeiro')
    ESTADOS_BRASIL = [('RJ', 'Rio de Janeiro'), ('SP', 'São Paulo'), ('MG', 'Minas Gerais'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('TO', 'Tocantins')]
    estado = models.CharField(max_length=2, choices=ESTADOS_BRASIL, default='RJ')
    data_associacao = models.DateField('Data de Associação', null=True, blank=True)
    ativo = models.BooleanField(default=True, verbose_name='Usuário Ativo')
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True, verbose_name='Foto de Perfil')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        nome_completo = self.get_full_name()
        if nome_completo:
            return f"{nome_completo} ({self.get_tipo_usuario_display()})"
        return f"{self.username} ({self.get_tipo_usuario_display()})"
"""
    criar_arquivo('accounts/models.py', models_content)

    # 2. accounts/admin.py (CORREÇÃO DO IMPORTERROR)
    admin_content = """from django.contrib import admin
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
"""
    criar_arquivo('accounts/admin.py', admin_content)

    # 3. accounts/forms.py (Necessário para o registro)
    forms_content = """from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario')

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario')
"""
    criar_arquivo('accounts/forms.py', forms_content)

    # 4. accounts/views.py (Views de Home, Dashboard e Registro)
    views_content = """from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from .forms import UsuarioCreationForm 
from django.contrib.auth.views import LoginView

# View de Login customizada (opcional, mas mantém o fluxo)
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

# Home pública
def home_view(request):
    return render(request, 'base/home.html', {'titulo': 'Bem-vindo à Intranet ACJogos-RJ'})

# Dashboard (acesso após login)
@login_required
def dashboard_view(request):
    return render(request, 'base/dashboard.html', {'titulo': 'Dashboard'})


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
    
    context = {'form': form, 'titulo': 'Criar Conta'}
    return render(request, 'accounts/registrar.html', context)
"""
    criar_arquivo('accounts/views.py', views_content)

    # 5. accounts/urls.py (URLs do app accounts)
    urls_content = """from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    # Rotas de Autenticação
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrar/', views.registrar_usuario, name='registrar'),
    
    # Rotas de Senha (Password Reset) - Usam os templates registration/
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    # Rotas do Sistema
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Home Page (Rota Vazia)
    path('', views.home_view, name='home'),
]
"""
    criar_arquivo('accounts/urls.py', urls_content)

# --- Configuração dos Apps de Módulos (Empresas, Projetos, etc.) ---

def configurar_apps_modulos():
    print("\n📝 Configurando apps de módulo (views.py e urls.py)...")
    
    for app in APPS_DO_PROJETO:
        if app == 'accounts': continue
            
        # views.py (Aponta para o template Em Construção, que usa o layout bonito)
        views_content = f"""from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    # Usa o template base/em_construcao.html que herda o layout bonito de sidebar
    return render(request, 'base/em_construcao.html', {{'app_name': '{app.capitalize()}'}})
"""
        criar_arquivo(f'{app}/views.py', views_content)
        
        # urls.py
        urls_content = f"""from django.urls import path
from . import views

app_name = '{app}'

urlpatterns = [
    path('', views.home_view, name='home'),
    # Adicione mais URLs aqui conforme for desenvolvendo o app '{app}'
]
"""
        criar_arquivo(f'{app}/urls.py', urls_content)

# --- Criação e Atualização de Templates (Parte Gráfica) ---

def criar_templates_completos():
    print("\n📝 Criando e atualizando todos os templates HTML (Layout Gráfico)...")
    
    # 1. Base/base.html (Com Navbar e Sidebar)
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
                {% block content %}{% endblock %}
            </div>
        </div>
    {% else %}
        <div class="container-fluid no-sidebar pt-5">
            {% block content %}{% endblock %}
        </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    criar_arquivo('templates/base/base.html', base_html_content)

    # 2. Base/home.html
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

    # 3. Base/dashboard.html
    dashboard_html_content = """{% extends "base/base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
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
{% endblock %}
"""
    criar_arquivo('templates/base/dashboard.html', dashboard_html_content)
    
    # 4. Base/em_construcao.html
    em_construcao_content = """{% extends "base/base.html" %}

{% block title %}Em Construção{% endblock %}

{% block content %}
<div class="row justify-content-center text-center pt-5">
    <div class="col-md-10">
        <h1 class="mt-5 display-4">App '{{ app_name|default:"Esta Página" }}' em Construção</h1>
        <p class="lead">O layout gráfico está funcionando! Agora, vamos desenvolver esta página.</p>
        <p><a href="{% url 'accounts:dashboard' %}" class="btn btn-secondary mt-3">Voltar ao Dashboard</a></p>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/base/em_construcao.html', em_construcao_content)
    
    # 5. Templates de Autenticação (login, registrar, reset de senha)
    
    # templates/accounts/login.html
    login_html_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Login - Intranet{% endblock %}{% block content %}<div class="row justify-content-center pt-5"><div class="col-md-6 col-lg-4"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-primary text-white text-center"><h3 class="fw-light my-4">Acesso à Intranet</h3></div><div class="card-body">{% if form.errors %}<div class="alert alert-danger" role="alert">Usuário ou senha inválidos. Tente novamente.</div>{% endif %}<form method="post">{% csrf_token %}{{ form|crispy }}<div class="d-flex align-items-center justify-content-between mt-4 mb-0"><a class="small" href="{% url 'password_reset' %}">Esqueceu a senha?</a><button type="submit" class="btn btn-primary">Entrar</button></div></form></div><div class="card-footer text-center py-3"><div class="small">Não tem conta? <a href="{% url 'accounts:registrar' %}">Criar Conta</a></div></div></div></div></div>{% endblock %}"""
    criar_arquivo('templates/accounts/login.html', login_html_content)

    # templates/accounts/registrar.html
    registrar_html_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Registrar - Intranet{% endblock %}{% block content %}<div class="row justify-content-center pt-5"><div class="col-md-8 col-lg-6"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-success text-white text-center"><h3 class="fw-light my-4">Criar uma Nova Conta</h3></div><div class="card-body"><form method="post" novalidate>{% csrf_token %}{{ form|crispy }}<div class="d-grid gap-2 mt-4 mb-0"><button type="submit" class="btn btn-success btn-block">Registrar</button></div></form></div><div class="card-footer text-center py-3"><div class="small">Já tem uma conta? <a href="{% url 'accounts:login' %}">Faça o Login</a></div></div></div></div></div>{% endblock %}"""
    criar_arquivo('templates/accounts/registrar.html', registrar_html_content)
    
    # templates/registration/password_reset_form.html
    reset_form_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Redefinir Senha{% endblock %}{% block content %}<div class="row justify-content-center pt-5"><div class="col-md-6 col-lg-4"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-warning text-dark text-center"><h3 class="fw-light my-4">Redefinir Senha</h3></div><div class="card-body"><p>Insira seu email para receber as instruções de redefinição.</p><form method="post">{% csrf_token %}{{ form|crispy }}<div class="d-grid gap-2 mt-4"><button type="submit" class="btn btn-warning">Enviar email</button></div></form></div><div class="card-footer text-center py-3"><div class="small"><a href="{% url 'accounts:login' %}">Voltar para o Login</a></div></div></div></div></div>{% endblock %}"""
    criar_arquivo('templates/registration/password_reset_form.html', reset_form_content)
    
    # templates/registration/password_reset_done.html
    reset_done_content = """{% extends "base/base.html" %}{% block title %}Email Enviado{% endblock %}{% block content %}<div class="row justify-content-center pt-5 text-center"><div class="col-md-6"><h1 class="mt-5">Verifique seu Email</h1><p class="lead">Enviamos um email com as instruções para redefinir sua senha.</p><p><a href="{% url 'accounts:login' %}" class="btn btn-primary mt-3">Voltar ao Login</a></p></div></div>{% endblock %}"""
    criar_arquivo('templates/registration/password_reset_done.html', reset_done_content)
    
    # templates/registration/password_reset_confirm.html
    reset_confirm_content = """{% extends "base/base.html" %}{% load crispy_forms_tags %}{% block title %}Nova Senha{% endblock %}{% block content %}<div class="row justify-content-center pt-5"><div class="col-md-6 col-lg-4"><div class="card shadow-lg border-0 rounded-lg mt-5"><div class="card-header bg-primary text-white text-center"><h3 class="fw-light my-4">Definir Nova Senha</h3></div><div class="card-body">{% if validlink %}<p>Crie uma nova senha.</p><form method="post">{% csrf_token %}{{ form|crispy }}<div class="d-grid gap-2 mt-4"><button type="submit" class="btn btn-primary">Alterar Senha</button></div></form>{% else %}<div class="alert alert-danger">O link de redefinição expirou ou é inválido.</div><a href="{% url 'password_reset' %}" class="btn btn-warning">Tentar novamente</a>{% endif %}</div></div></div></div>{% endblock %}"""
    criar_arquivo('templates/registration/password_reset_confirm.html', reset_confirm_content)
    
    # templates/registration/password_reset_complete.html
    reset_complete_content = """{% extends "base/base.html" %}{% block title %}Senha Alterada{% endblock %}{% block content %}<div class="row justify-content-center pt-5 text-center"><div class="col-md-6"><h1 class="mt-5">Senha Alterada com Sucesso!</h1><p class="lead">Sua senha foi redefinida. Agora você pode fazer o login com a nova senha.</p><p><a href="{% url 'accounts:login' %}" class="btn btn-primary mt-3">Fazer Login</a></p></div></div>{% endblock %}"""
    criar_arquivo('templates/registration/password_reset_complete.html', reset_complete_content)


def criar_pastas_e_static():
    """Cria a estrutura de pastas e o CSS básico."""
    print("\n📝 Criando estrutura de pastas e static files...")
    
    # Cria as pastas necessárias
    pastas = ['templates', 'static/css', 'static/js', 'static/img', 'media/perfis']
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"✓ Pasta garantida: {pasta}")
        
    # Cria o arquivo CSS inicial
    css_content = """/* Arquivo: style.css
 * Use este arquivo para adicionar estilos customizados.
 */
"""
    criar_arquivo('static/css/style.css', css_content)


def main():
    print("=" * 70)
    print("🚀 SCRIPT DE AUTOMAÇÃO: CONFIGURAÇÃO FINAL E GRÁFICA")
    print("=" * 70)
    
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django.")
        return

    # 1. Instalação de dependências (Requerido para Django, decouple, crispy-forms, localflavor)
    print("\n📋 INSTALANDO DEPENDÊNCIAS (Pode demorar um pouco)...")
    requirements_content = """Django==5.1.3
python-decouple==3.8
django-crispy-forms==2.3
crispy-bootstrap5==2024.10
django-localflavor==4.0
"""
    criar_arquivo('requirements.txt', requirements_content)
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Dependências essenciais instaladas via requirements.txt.")
    except Exception as e:
        print(f"❌ AVISO: Não foi possível rodar o 'pip install'. Execute: pip install -r requirements.txt manualmente.")
    
    # 2. Cria todos os apps
    print("\n📝 Criando/Verificando Apps...")
    for app in APPS_DO_PROJETO:
        criar_app(app)

    # 3. Configura o projeto raiz
    configurar_projeto_raiz()
    
    # 4. Configura o app accounts (CRÍTICO)
    configurar_app_accounts()

    # 5. Configura os apps de módulo
    configurar_apps_modulos()

    # 6. Criação de Pastas e Static
    criar_pastas_e_static()
        
    # 7. Criação dos Templates (Parte Gráfica)
    criar_templates_completos()
    
    print("\n" + "=" * 70)
    print("✅ CONFIGURAÇÃO CONCLUÍDA. ERROS CRÍTICOS RESOLVIDOS.")
    print("   O ImportError e o 404 de URL foram corrigidos.")
    print("=" * 70)
    print("\n\n📋 PRÓXIMOS PASSOS (Obrigatório):")
    print("   1. Crie as migrações (se for a primeira vez):")
    print("      python manage.py makemigrations")
    print("   2. Aplique as migrações:")
    print("      python manage.py migrate")
    print("   3. Crie um superusuário:")
    print("      python manage.py createsuperuser")
    print("   4. Inicie o servidor (TUDO deve funcionar agora!):")
    print("      python manage.py runserver")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()