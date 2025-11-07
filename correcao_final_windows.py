#!/usr/bin/env python
"""
Script de Correção Completa - ACJogos Intranet (Windows Fix)
Execute na pasta raiz do projeto Django
"""

import os
import subprocess
import shutil
from pathlib import Path

def limpar_arquivo_se_necessario(caminho):
    """Remove arquivo se existir no lugar de uma pasta"""
    if os.path.exists(caminho) and os.path.isfile(caminho):
        print(f"⚠ Removendo arquivo conflitante: {caminho}")
        os.remove(caminho)

def criar_arquivo(caminho, conteudo):
    """Cria arquivo garantindo que a pasta existe"""
    pasta = os.path.dirname(caminho)
    
    # Verifica se há arquivos no caminho que deveriam ser pastas
    partes = pasta.split(os.sep)
    caminho_parcial = ""
    for parte in partes:
        if caminho_parcial:
            caminho_parcial = os.path.join(caminho_parcial, parte)
        else:
            caminho_parcial = parte
            
        if caminho_parcial and os.path.exists(caminho_parcial) and os.path.isfile(caminho_parcial):
            print(f"⚠ Removendo arquivo conflitante: {caminho_parcial}")
            os.remove(caminho_parcial)
    
    # Agora cria as pastas
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ {caminho}")

def criar_apps():
    """Cria todos os apps necessários"""
    print("\n📦 Criando apps...")
    apps = ['accounts', 'empresas', 'projetos', 'pesquisas', 'links']
    
    for app in apps:
        if not os.path.exists(app):
            try:
                subprocess.run(['python', 'manage.py', 'startapp', app], 
                             check=True, stdout=subprocess.DEVNULL)
                print(f"✓ App '{app}' criado")
            except:
                print(f"⚠ App '{app}' - erro ao criar (pode já existir)")
        else:
            print(f"• App '{app}' já existe")

def criar_settings():
    """Cria settings.py correto"""
    print("\n⚙️  Configurando settings.py...")
    
    settings_content = """import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', 
                       cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
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

DB_ENGINE = config('DB_ENGINE', default='sqlite')
if DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'accounts.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:home'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

EMAIL_BACKEND = config('EMAIL_BACKEND', 
                       default='django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', 
                            default='noreply@acjogos-rj.org.br')

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
"""
    criar_arquivo('acjogos_intranet/settings.py', settings_content)

def criar_urls_principal():
    """Cria URLs principal do projeto"""
    print("\n🔗 Configurando URLs...")
    
    urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('empresas/', include('empresas.urls')),
    path('projetos/', include('projetos.urls')),
    path('pesquisas/', include('pesquisas.urls')),
    path('links/', include('links.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    criar_arquivo('acjogos_intranet/urls.py', urls_content)

def criar_models_accounts():
    """Cria modelo Usuario"""
    print("\n👤 Configurando modelo Usuario...")
    
    models_content = """from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.br.models import BRCPFField, BRPostalCodeField

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('DIRETORIA', 'Diretoria'),
        ('ASSOCIADO', 'Associado'),
        ('AFILIADO', 'Afiliado'),
        ('COLETIVO', 'Coletivo/Institucional'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, 
                                     default='AFILIADO', verbose_name='Tipo de Usuário')
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
    
    ESTADOS_BRASIL = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
        ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]
    estado = models.CharField(max_length=2, choices=ESTADOS_BRASIL, default='RJ')
    
    data_associacao = models.DateField('Data de Associação', null=True, blank=True)
    ativo = models.BooleanField(default=True, verbose_name='Usuário Ativo')
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True, 
                                     verbose_name='Foto de Perfil')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        nome = self.get_full_name()
        return f"{nome or self.username} ({self.get_tipo_usuario_display()})"
"""
    criar_arquivo('accounts/models.py', models_content)

def criar_forms_accounts():
    """Cria formulários"""
    forms_content = """from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario')
"""
    criar_arquivo('accounts/forms.py', forms_content)

def criar_admin_accounts():
    """Cria admin"""
    admin_content = """from django.contrib import admin
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
"""
    criar_arquivo('accounts/admin.py', admin_content)

def criar_views_accounts():
    """Cria views do accounts"""
    views_content = """from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm

def home_view(request):
    return render(request, 'base/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'base/dashboard.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = UsuarioCreationForm()
    return render(request, 'accounts/registrar.html', {'form': form})
"""
    criar_arquivo('accounts/views.py', views_content)

def criar_urls_accounts():
    """Cria URLs do accounts"""
    urls_content = """from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrar/', views.registrar_usuario, name='registrar'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
"""
    criar_arquivo('accounts/urls.py', urls_content)

def criar_apps_modulos():
    """Cria views e URLs dos outros apps"""
    print("\n📋 Configurando apps de módulos...")
    
    apps = ['empresas', 'projetos', 'pesquisas', 'links']
    
    for app in apps:
        # Views
        views_content = f"""from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'base/em_construcao.html', {{'app_name': '{app.capitalize()}'}})
"""
        criar_arquivo(f'{app}/views.py', views_content)
        
        # URLs
        urls_content = f"""from django.urls import path
from . import views

app_name = '{app}'

urlpatterns = [
    path('', views.home_view, name='home'),
]
"""
        criar_arquivo(f'{app}/urls.py', urls_content)

def limpar_templates_conflitantes():
    """Remove arquivos conflitantes na pasta templates"""
    print("\n🧹 Limpando arquivos conflitantes...")
    
    pastas_templates = [
        'templates',
        'templates/base',
        'templates/accounts',
        'templates/registration'
    ]
    
    for pasta in pastas_templates:
        if os.path.exists(pasta) and os.path.isfile(pasta):
            print(f"⚠ Removendo arquivo: {pasta}")
            os.remove(pasta)
    
    # Cria as pastas
    for pasta in pastas_templates:
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"✓ Pasta garantida: {pasta}")

def criar_templates():
    """Cria todos os templates HTML"""
    print("\n🎨 Criando templates HTML...")
    
    # Limpa conflitos primeiro
    limpar_templates_conflitantes()
    
    # Base template
    base_html = """{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ACJogos Intranet{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    {% if user.is_authenticated and request.resolver_match.url_name not in 'home,login,registrar' %}
        {% include 'base/navbar.html' %}
        <div class="container-fluid">
            <div class="row">
                {% include 'base/sidebar.html' %}
                <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 main-content">
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert {{ message.tags }} alert-dismissible fade show mt-3" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                    {% block content %}{% endblock %}
                </main>
            </div>
        </div>
    {% else %}
        <div class="container-fluid">
            {% if messages %}
                {% for message in messages %}
                    <div class="alert {{ message.tags }} alert-dismissible fade show mt-3" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
            {% block content %}{% endblock %}
        </div>
    {% endif %}
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
"""
    criar_arquivo('templates/base/base.html', base_html)
    
    # Navbar
    navbar_html = """<nav class="navbar navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'accounts:dashboard' %}">
            <i class="bi bi-controller"></i> ACJogos Intranet
        </a>
        <div class="d-flex align-items-center">
            <span class="text-white me-3">
                <i class="bi bi-person-circle"></i> {{ user.get_full_name|default:user.username }}
            </span>
            <div class="dropdown">
                <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" 
                        data-bs-toggle="dropdown">
                    Menu
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="{% url 'admin:index' %}">
                        <i class="bi bi-gear"></i> Admin</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item text-danger" href="{% url 'accounts:logout' %}">
                        <i class="bi bi-box-arrow-right"></i> Sair</a></li>
                </ul>
            </div>
        </div>
    </div>
</nav>
"""
    criar_arquivo('templates/base/navbar.html', navbar_html)
    
    # Sidebar
    sidebar_html = """<nav id="sidebar" class="col-md-3 col-lg-2 d-md-block bg-dark sidebar">
    <div class="position-sticky pt-5 mt-3">
        <ul class="nav flex-column">
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}" 
                   href="{% url 'accounts:dashboard' %}">
                    <i class="bi bi-house-door"></i> Dashboard
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.namespace == 'empresas' %}active{% endif %}" 
                   href="{% url 'empresas:home' %}">
                    <i class="bi bi-building"></i> Empresas
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.namespace == 'projetos' %}active{% endif %}" 
                   href="{% url 'projetos:home' %}">
                    <i class="bi bi-folder"></i> Projetos
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.namespace == 'pesquisas' %}active{% endif %}" 
                   href="{% url 'pesquisas:home' %}">
                    <i class="bi bi-clipboard-data"></i> Pesquisas
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.namespace == 'links' %}active{% endif %}" 
                   href="{% url 'links:home' %}">
                    <i class="bi bi-link-45deg"></i> Links Úteis
                </a>
            </li>
        </ul>
    </div>
</nav>
"""
    criar_arquivo('templates/base/sidebar.html', sidebar_html)
    
    # Home
    home_html = """{% extends "base/base.html" %}
{% block title %}Bem-vindo - ACJogos{% endblock %}
{% block content %}
<div class="container">
    <div class="row min-vh-100 align-items-center">
        <div class="col-md-8 mx-auto text-center">
            <div class="hero-section">
                <i class="bi bi-controller display-1 text-primary mb-4"></i>
                <h1 class="display-3 fw-bold mb-4">ACJogos-RJ</h1>
                <p class="lead mb-5">Sistema de Gestão Interna da Associação Cultural de Jogos do Rio de Janeiro</p>
                <div class="d-grid gap-3 d-sm-flex justify-content-sm-center">
                    <a href="{% url 'accounts:login' %}" class="btn btn-primary btn-lg px-5">
                        <i class="bi bi-box-arrow-in-right"></i> Entrar
                    </a>
                    <a href="{% url 'accounts:registrar' %}" class="btn btn-outline-primary btn-lg px-5">
                        <i class="bi bi-person-plus"></i> Criar Conta
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/base/home.html', home_html)
    
    # Dashboard
    dashboard_html = """{% extends "base/base.html" %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2"><i class="bi bi-speedometer2"></i> Dashboard</h1>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card text-white bg-primary">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="card-title">Empresas</h6>
                        <h2 class="mb-0">120</h2>
                    </div>
                    <i class="bi bi-building display-4"></i>
                </div>
            </div>
            <div class="card-footer bg-primary bg-opacity-75">
                <a href="{% url 'empresas:home' %}" class="text-white text-decoration-none small">
                    Ver detalhes <i class="bi bi-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>
    
    <div class="col-md-3">
        <div class="card text-white bg-success">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="card-title">Projetos</h6>
                        <h2 class="mb-0">45</h2>
                    </div>
                    <i class="bi bi-folder display-4"></i>
                </div>
            </div>
            <div class="card-footer bg-success bg-opacity-75">
                <a href="{% url 'projetos:home' %}" class="text-white text-decoration-none small">
                    Ver projetos <i class="bi bi-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>
    
    <div class="col-md-3">
        <div class="card text-white bg-warning">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="card-title">Pesquisas</h6>
                        <h2 class="mb-0">5</h2>
                    </div>
                    <i class="bi bi-clipboard-data display-4"></i>
                </div>
            </div>
            <div class="card-footer bg-warning bg-opacity-75">
                <a href="{% url 'pesquisas:home' %}" class="text-white text-decoration-none small">
                    Responder <i class="bi bi-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>
    
    <div class="col-md-3">
        <div class="card text-white bg-info">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="card-title">Seu Perfil</h6>
                        <p class="mb-0 small">{{ user.get_tipo_usuario_display }}</p>
                    </div>
                    <i class="bi bi-person-badge display-4"></i>
                </div>
            </div>
            <div class="card-footer bg-info bg-opacity-75">
                <span class="text-white small">{{ user.email }}</span>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header bg-light">
                <h5 class="mb-0"><i class="bi bi-info-circle"></i> Bem-vindo!</h5>
            </div>
            <div class="card-body">
                <p>Olá, <strong>{{ user.get_full_name|default:user.username }}</strong>!</p>
                <p>Use o menu lateral para navegar pelas diferentes áreas do sistema.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    criar_arquivo('templates/base/dashboard.html', dashboard_html)
    
    # Em construção
    em_construcao_html = """{% extends "base/base.html" %}
{% block title %}{{ app_name }} - Em Construção{% endblock %}
{% block content %}
<div class="text-center py-5">
    <i class="bi bi-tools display-1 text-muted mb-4"></i>
    <h1 class="display-4 mb-3">{{ app_name }} em Construção</h1>
    <p class="lead text-muted mb-4">Esta área está sendo desenvolvida.</p>
    <a href="{% url 'accounts:dashboard' %}" class="btn btn-primary">
        <i class="bi bi-arrow-left"></i> Voltar ao Dashboard
    </a>
</div>
{% endblock %}
"""
    criar_arquivo('templates/base/em_construcao.html', em_construcao_html)
    
    # Login
    login_html = """{% extends "base/base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="text-center py-5">
    <h1 class="display-4 mb-3">Login</h1>
    <p class="lead text-muted mb-4">Acesse sua conta</p>
    <form method="post">
        {% csrf_token %}
        <div class="mb-3">
            <label for="username" class="form-label">Usuário</label>
            <input type="text" class="form-control" id="username" name="username" required>
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Senha</label>
            <input type="password" class="form-control" id="password" name="password" required>
        </div>
        <button type="submit" class="btn btn-primary">Entrar</button>
    </form>
</div>
{% endblock %}
"""
    criar_arquivo('templates/base/login.html', login_html)