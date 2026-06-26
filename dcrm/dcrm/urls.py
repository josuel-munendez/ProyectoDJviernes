from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE: Agregar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('', include('website.urls')),
    path('productos/', include('productos.urls')),
    path('catalogo/', include('catalogo.urls')),
]