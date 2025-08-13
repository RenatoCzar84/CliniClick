from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.base.urls')),
    path('usuarios/', include(('apps.usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('medicos/', include('apps.medicos.urls')),

    # >>> ROTA DE AGENDAMENTO (placeholder), protegida por login <<<
    path(
        'agendamento/',
        login_required(TemplateView.as_view(template_name='base/agendamento.html')),
        name='agendamento'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


