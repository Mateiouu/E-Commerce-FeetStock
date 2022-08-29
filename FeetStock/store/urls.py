from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import  *
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.home, name = 'home'),
	
	   path('aboutus', views.about, name = "about"),
    path('tienda/', views.store, name = "store"),
    path('hombre/', views.hombre, name = "hombre"),
    path('mujer/', views.mujer, name = "mujer"),
    path('ninio/', views.ninio, name = "ninio"),
	path('cart/', views.cart, name="cart"),
	path('product/<str:pk>/', views.product, name="product"),
    path('eliminaritem/<int:id>', views.eliminaritem, name = 'eliminaritem'),
    path('crear-producto/', ProductoCreate.as_view(), name = 'crear'),
    path('editar-producto/<int:pk>', ProductoUpdate.as_view(), name = 'editar'),
    path('eliminar-producto/<int:pk>', ProductoDelete.as_view(), name = 'eliminar'),
    path('process-order/', processOrder, name = 'compra'),
    path('nohaycont/', nohaycontenido, name = 'nohaycont'),
 

]   


urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
