from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App de autenticação (accounts)
    path('', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Outros apps
    path('empresas/', include(('empresas.urls', 'empresas'), namespace='empresas')),
    path('projetos/', include(('projetos.urls', 'projetos'), namespace='projetos')),
    path('pesquisas/', include(('pesquisas.urls', 'pesquisas'), namespace='pesquisas')),
    path('links/', include(('links.urls', 'links'), namespace='links')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
