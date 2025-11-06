from django.contrib import admin
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
