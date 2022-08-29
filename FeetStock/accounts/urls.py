from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from store.views import *
from .views import *

urlpatterns = [
	path('', home, name = 'home'),
    path('tienda/', store, name = "store"),
    path('login/', views.loginView, name = "login"),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
    path('signup/', views.registerView, name = 'register'),
    path('password/', CambiarContraView.as_view(template_name = 'change_password.html')),
    path('editar_perfil/', UserEditView.as_view(), name = 'editar-perfil'),
    path('ordenes/', userpage, name = "ordenes"),
]

urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    