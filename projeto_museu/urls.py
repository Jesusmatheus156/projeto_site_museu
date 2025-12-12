from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Interface administrativa
    path('admin/', admin.site.urls),
    # Rota para o arquivo urls.py da aplicação base
    path('', include('base.urls')),
    # Rota para o arquivo urls.py da aplicação usuario
    # Rota para o sistema de tradução do Django
    path('i18n/', include('django.conf.urls.i18n')), # <-- Rota para o Django processar a troca
]

# Opcional: Para incluir o código do idioma na URL (ex: /en/home/)
urlpatterns += i18n_patterns(
    path('', include('base.urls')),

)

# ESSENCIAL: Serve arquivos de MÍDIA no modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)