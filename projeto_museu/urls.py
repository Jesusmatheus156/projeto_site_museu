from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

# 1. ROTAS FIXAS (Não mudam de idioma e não ganham /en-us/ na URL)
urlpatterns = [
    # Rota para o sistema de troca de idioma do Django
    path('i18n/', include('django.conf.urls.i18n')), 
]

# 2. ROTAS TRADUZIDAS (Ganham o prefixo /pt-br/, /en-us/ ou /es/)
urlpatterns += i18n_patterns(
    # Interface administrativa
    path('admin/', admin.site.urls),
    # Rota para o arquivo urls.py da aplicação base
    path('', include('base.urls')),
)

# 3. ESSENCIAL: Serve arquivos de MÍDIA no modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)