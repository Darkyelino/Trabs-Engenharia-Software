# webgenda/urls.py

from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from agenda.views import register_view  # Sua view de registro customizada
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='agenda/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registrar/', register_view, name='registrar'),

    path('perfil/mudar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='agenda/password_change_form.html',
        success_url=reverse_lazy('password_change_done')
    ), name='password_change'),
    path('perfil/mudar-senha/concluido/', auth_views.PasswordChangeDoneView.as_view(
        template_name='agenda/password_change_done.html'
    ), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='agenda/password_reset_form.html',
        email_template_name='agenda/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='agenda/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='agenda/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='agenda/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('', include('agenda.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)