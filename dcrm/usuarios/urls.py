from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.register_usuario, name="register_usuario"),
    path("perfil/", views.perfil, name="perfil"),
]
