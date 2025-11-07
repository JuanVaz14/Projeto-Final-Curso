#!/usr/bin/env python
"""
Script para corrigir automaticamente o projeto ACJogos Intranet
Execute este script na pasta raiz do projeto Django
"""

import os
from pathlib import Path

def criar_arquivo(caminho, conteudo):
    """Cria ou sobrescreve um arquivo com o conteúdo fornecido"""
    pasta = os.path.dirname(caminho)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"✓ Pasta criada: {pasta}")
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✓ Arquivo criado/atualizado: {caminho}")

def main():
    print("=" * 60)
    print("🔧 CORREÇÃO AUTOMÁTICA DO PROJETO ACJOGOS INTRANET")
    print("=" * 60)
    print()
    
    # Verifica se está na pasta correta
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Este script deve ser executado na pasta raiz do projeto Django")
        print("   (onde está o arquivo manage.py)")
        return
    
    print("✓ Pasta do projeto detectada!")
    print()
    
    # 1. Arquivo .env
    print("📝 Criando arquivo .env...")
    env_content = """# Django Settings
SECRET_KEY=django-insecure-test-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
# Para SQLite (desenvolvimento), use:
DB_ENGINE=sqlite

# Para PostgreSQL (produção), descomente e configure:
# DB_ENGINE=postgresql
# DB_NAME=acjogos_db
# DB_USER=postgres
# DB_PASSWORD=sua_senha_aqui
# DB_HOST=localhost
# DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@acjogos-rj.org.br
"""
    criar_arquivo('.env', env_content)
    
    # 2. Arquivo requirements.txt
    print("\n📝 Criando arquivo requirements.txt...")
    requirements_content = """# Django Core
Django==5.1.3
django-localflavor==4.0
python-decouple==3.8

# Database
psycopg2-binary==2.9.9

# Image handling
Pillow==11.0.0

# API Integration
requests==2.32.3

# Excel/PDF exports
openpyxl==3.1.5
reportlab==4.2.5
xlsxwriter==3.2.0

# Forms
django-crispy-forms==2.3
crispy-bootstrap5==2024.10

# API REST (opcional para futuras integrações)
djangorestframework==3.15.2

# Ferramentas de desenvolvimento
ipython==8.29.0
django-debug-toolbar==4.4.6

# Segurança
django-cors-headers==4.6.0

# Mapa (opcional)
django-leaflet==0.30.1
"""
    criar_arquivo('requirements.txt', requirements_content)
    
    # 3. Arquivo settings.py
    print("\n📝 Atualizando acjogos_intranet/settings.py...")
    settings_content = """import os
from pathlib import Path
from decouple import config

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
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
    'rest_framework',
    
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

# Database - Configuração flexível
DB_ENGINE = config('DB_ENGINE', default='sqlite')

if DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='acjogos_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='postgres'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    # SQLite para desenvolvimento
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.Usuario'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

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
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email Configuration
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@acjogos-rj.org.br')

# Security Settings (Production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Configurações de upload
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Mensagens
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
    
    # 4. Arquivo models.py do app accounts
    print("\n📝 Atualizando accounts/models.py...")
    models_content = """from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.br.models import BRCPFField, BRPostalCodeField
from django.core.validators import RegexValidator


class Usuario(AbstractUser):
    \"\"\"
    Modelo customizado de usuário com tipos específicos para ACJogos-RJ
    \"\"\"
    TIPO_USUARIO = [
        ('DIRETORIA', 'Diretoria'),
        ('ASSOCIADO', 'Associado'),
        ('AFILIADO', 'Afiliado'),
        ('COLETIVO', 'Coletivo/Institucional'),
    ]
    
    # Informações básicas
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=TIPO_USUARIO,
        default='AFILIADO',
        verbose_name='Tipo de Usuário'
    )
    nome_social = models.CharField(
        max_length=150, 
        blank=True,
        verbose_name='Nome Social'
    )
    cpf = BRCPFField(
        'CPF', 
        unique=True, 
        null=True, 
        blank=True,
        help_text='Formato: 000.000.000-00'
    )
    
    # Contato
    telefone_validator = RegexValidator(
        regex=r'^\\+?1?\\d{9,15}$',
        message="Telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    telefone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[telefone_validator],
        help_text='Formato: (21) 99999-9999'
    )
    nick_discord = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Nick no Discord'
    )
    
    # Endereço
    cep = BRPostalCodeField(
        'CEP', 
        blank=True,
        help_text='Formato: 00000-000'
    )
    endereco = models.CharField(
        'Endereço', 
        max_length=255, 
        blank=True
    )
    numero = models.CharField(
        'Número', 
        max_length=10, 
        blank=True
    )
    complemento = models.CharField(
        max_length=100, 
        blank=True
    )
    bairro = models.CharField(
        max_length=100, 
        blank=True
    )
    cidade = models.CharField(
        max_length=100, 
        blank=True,
        default='Rio de Janeiro'
    )
    
    ESTADOS_BRASIL = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]
    
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_BRASIL,
        default='RJ'
    )
    
    # Campos de controle
    data_associacao = models.DateField(
        'Data de Associação', 
        null=True, 
        blank=True,
        help_text='Data de ingresso na associação'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Usuário Ativo'
    )
    foto_perfil = models.ImageField(
        upload_to='perfis/', 
        blank=True, 
        null=True,
        verbose_name='Foto de Perfil'
    )
    
    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['tipo_usuario']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        nome_completo = self.get_full_name()
        if nome_completo:
            return f"{nome_completo} ({self.get_tipo_usuario_display()})"
        return f"{self.username} ({self.get_tipo_usuario_display()})"
    
    def get_nome_exibicao(self):
        \"\"\"Retorna nome social se disponível, senão nome completo\"\"\"
        if self.nome_social:
            return self.nome_social
        return self.get_full_name() or self.username
    
    def is_diretoria(self):
        \"\"\"Verifica se usuário é da diretoria\"\"\"
        return self.tipo_usuario == 'DIRETORIA'
    
    def is_associado(self):
        \"\"\"Verifica se usuário é associado (inclui diretoria)\"\"\"
        return self.tipo_usuario in ['DIRETORIA', 'ASSOCIADO']
    
    def is_afiliado(self):
        \"\"\"Verifica se usuário é afiliado\"\"\"
        return self.tipo_usuario == 'AFILIADO'
    
    def is_coletivo(self):
        \"\"\"Verifica se usuário representa um coletivo/instituição\"\"\"
        return self.tipo_usuario == 'COLETIVO'
    
    def can_edit_empresa(self, empresa):
        \"\"\"Verifica se o usuário pode editar determinada empresa\"\"\"
        if self.is_diretoria():
            return True
        if self.tipo_usuario == 'ASSOCIADO':
            return empresa.responsavel == self
        return False
    
    def get_endereco_completo(self):
        \"\"\"Retorna endereço formatado\"\"\"
        if not self.endereco:
            return ''
        
        partes = [self.endereco]
        if self.numero:
            partes.append(f"nº {self.numero}")
        if self.complemento:
            partes.append(self.complemento)
        if self.bairro:
            partes.append(self.bairro)
        if self.cidade and self.estado:
            partes.append(f"{self.cidade}/{self.estado}")
        if self.cep:
            partes.append(f"CEP: {self.cep}")
        
        return ', '.join(partes)
"""
    criar_arquivo('accounts/models.py', models_content)
    
    # 5. Criar pastas necessárias
    print("\n📁 Criando estrutura de pastas...")
    pastas = [
        'static',
        'media',
        'media/perfis',
        'templates',
        'staticfiles',
    ]
    
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"✓ Pasta criada: {pasta}")
        else:
            print(f"• Pasta já existe: {pasta}")
    
    # 6. Criar .gitignore
    print("\n📝 Criando arquivo .gitignore...")
    gitignore_content = """# Python
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static

# Environment
.env
.venv
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""
    criar_arquivo('.gitignore', gitignore_content)
    
    print("\n" + "=" * 60)
    print("✅ CORREÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("\n1. Instale as dependências:")
    print("   pip install -r requirements.txt")
    print("\n2. Crie as migrações:")
    print("   python manage.py makemigrations")
    print("\n3. Aplique as migrações:")
    print("   python manage.py migrate")
    print("\n4. Crie um superusuário:")
    print("   python manage.py createsuperuser")
    print("\n5. Inicie o servidor:")
    print("   python manage.py runserver")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()