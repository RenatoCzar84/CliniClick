"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.base import views as base_views
from apps.usuarios import views as uviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.base.urls')),
    path("agenda/", include(("apps.agenda.urls", "agenda"), namespace="agenda")),
    path('usuarios/', include(('apps.usuarios.urls', 'usuarios'), namespace='usuarios')),
    path("usuarios/login/", uviews.login_usuario, name="login_usuario"),
]

# Servir arquivos estáticos durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
