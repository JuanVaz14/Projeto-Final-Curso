from django.contrib import admin
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
