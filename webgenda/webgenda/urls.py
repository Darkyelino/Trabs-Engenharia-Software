"""
URL configuration for webgenda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from agenda.views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registrar/', register_view, name='registrar'),

    path('perfil/mudar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='agenda/password_change_form.html',
        success_url='/perfil/mudar-senha/concluido/'
    ), name='password_change'),
    path('perfil/mudar-senha/concluido/', auth_views.PasswordChangeDoneView.as_view(
        template_name='agenda/password_change_done.html'
    ), name='password_change_done'),

    path('', include('agenda.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)