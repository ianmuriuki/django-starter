from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Include app URLs (your main app, like 'app.urls')
    path('', include('app.urls')),
    
    # Admin URLs for accessing the Django admin panel
    path('admin/', admin.site.urls),
    
    # Allauth URLs for authentication (registration, login, logout, etc.)
    path('accounts/', include('allauth.urls')),
    
    # Custom authentication-related URLs (login, logout, password reset, etc.)
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customizing the Django Admin site
SITE_NAME = "Django Starter Template"
admin.site.site_header = SITE_NAME
admin.site.index_title = SITE_NAME + " Dashboard"
admin.site.site_title = SITE_NAME + " Dashboard"
