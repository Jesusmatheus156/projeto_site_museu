from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

# Rotas que NÃO mudam com o idioma
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Rotas que mudam (ganham /pt-br/, /en/, /es/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    prefix_default_language=True # Isso ajuda a evitar confusão no redirecionamento
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)