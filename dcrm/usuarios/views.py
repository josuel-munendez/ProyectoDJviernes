"""Vistas de la aplicación usuarios.

Maneja el registro de nuevos usuarios, visualización y edición del perfil.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from core.validators import RegexValidator
from .forms import UserRegistrationForm
from .models import UserProfile


def register_usuario(request: HttpRequest) -> HttpResponse:
    """Registra un nuevo usuario en el sistema.

    Valida los campos con expresiones regulares, autentica al usuario
    y redirige a la página principal si el registro es exitoso.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Validación adicional con expresiones regulares
            if not RegexValidator.validate("username", username):
                messages.error(request, "El usuario contiene caracteres no permitidos")
                return render(request, "usuarios/register.html", {"form": form})
            if not RegexValidator.validate("password", password):
                messages.error(request, "La contrasena no cumple los requisitos")
                return render(request, "usuarios/register.html", {"form": form})
            form.save()
            # Autenticación automática después del registro
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, "Usuario registrado exitosamente")
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "usuarios/register.html", {"form": form})


@login_required
def perfil(request: HttpRequest) -> HttpResponse:
    """Muestra el perfil del usuario autenticado."""
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    return render(request, "usuarios/perfil.html", {"profile": profile})


@login_required
def editar_perfil(request: HttpRequest) -> HttpResponse:
    """Permite al usuario editar su teléfono y dirección."""
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == "POST":
        telefono = request.POST.get("telefono", "")
        direccion = request.POST.get("direccion", "")
        profile.telefono = telefono
        profile.direccion = direccion
        profile.save()
        messages.success(request, "Perfil actualizado exitosamente")
        return redirect("perfil")
    return render(request, "usuarios/editar_perfil.html", {"profile": profile})
