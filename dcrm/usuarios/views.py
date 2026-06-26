from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from core.validators import RegexValidator
from .forms import UserRegistrationForm
from .models import UserProfile


def register_usuario(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if not RegexValidator.validate("username", username):
                messages.error(request, "El usuario contiene caracteres no permitidos")
                return render(request, "usuarios/register.html", {"form": form})
            if not RegexValidator.validate("password", password):
                messages.error(request, "La contrasena no cumple los requisitos")
                return render(request, "usuarios/register.html", {"form": form})
            form.save()
            messages.success(request, "Usuario registrado exitosamente")
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "usuarios/register.html", {"form": form})


@login_required
def perfil(request: HttpRequest) -> HttpResponse:
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    return render(request, "usuarios/perfil.html", {"profile": profile})
