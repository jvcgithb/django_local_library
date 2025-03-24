"""
URL configuration for locallibrary project.

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
from django.urls import path
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Use include() to add paths from the catalog application
from django.urls import include

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    # Ruta de inicio de sesión
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    
    # Ruta de cierre de sesión
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Ruta para cambiar la contraseña
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    
    # Ruta que se muestra después de cambiar la contraseña
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    # Ruta para restablecer la contraseña
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    # Ruta que se muestra después de solicitar el restablecimiento de contraseña
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    # Ruta para confirmar el restablecimiento de la contraseña
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Ruta que se muestra después de completar el restablecimiento de contraseña
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Ruta para la lista de libros en posesión
    path('catalog/mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

    # Ruta para bibliotecarios
    path('catalog/borrowed/', views.LoanedBooksListView.as_view(), name='all-borrowed'),

    # Ruta para renovar prestamos
    path('catalog/book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]