from django.urls import path, include
from django.conf.urls import handler404, handler500

from .admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('usuarios.urls')),
    path('', include('website.urls')),
    path('productos/', include('productos.urls')),
    path('catalogo/', include('catalogo.urls')),
]