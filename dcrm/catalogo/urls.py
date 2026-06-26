from django.urls import path
from . import views

app_name = "catalogo"
urlpatterns = [
    path("categorias/", views.listado_categorias, name="categorias"),
    path("", views.listado_catalogos, name="catalogos"),
]
