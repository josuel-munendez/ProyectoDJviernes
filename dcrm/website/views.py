from typing import Any
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.services import CrudService
from core.validators import RegexValidator
from .forms import LoginForm, RecordForm, UserRegisterForm
from .models import Record


_record_service = CrudService(Record)


def home(request: HttpRequest) -> HttpResponse:
    records_queryset: QuerySet = _record_service.get_all()
    paginator: Paginator = Paginator(records_queryset, 5)
    page_number: str | None = request.GET.get("page")
    records_page: Page = paginator.get_page(page_number)

    if request.method == "POST":
        form: LoginForm = LoginForm(request, data=request.POST)
        if form.is_valid():
            user: User = form.get_user()
            login(request, user)
            messages.success(request, "Acceso realizado exitosamente")
            return redirect("home")
        messages.error(request, "Las credenciales no son validas")

    return render(request, "home.html", {"records": records_page})


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: LoginForm = LoginForm(request, data=request.POST)
        if form.is_valid():
            user: User = form.get_user()
            login(request, user)
            messages.success(request, "Acceso realizado exitosamente")
            return redirect("home")
        messages.error(request, "Las credenciales no son validas")
    else:
        form: LoginForm = LoginForm()

    return render(request, "home.html", {"form": form})


@login_required
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, "Cerraste la sesion correctamente")
    return redirect("home")


@login_required
def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: UserRegisterForm = UserRegisterForm(request.POST)

        if form.is_valid():
            username: str = form.cleaned_data["username"]
            if not RegexValidator.validate("username", username):
                messages.error(request, "El nombre de usuario contiene caracteres no permitidos")
                return render(request, "register.html", {"form": form})

            password: str = form.cleaned_data["password1"]
            if not RegexValidator.validate("password", password):
                messages.error(request, "La contrasena no cumple con los requisitos de seguridad")
                return render(request, "register.html", {"form": form})

            form.save()
            user: User | None = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, "Registro exitoso")
            return redirect("home")
    else:
        form: UserRegisterForm = UserRegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def customer_record(request: HttpRequest, pk: str) -> HttpResponse:
    customer_record: Record = get_object_or_404(Record, id=pk)
    return render(request, "record.html", {"customer_record": customer_record})


@login_required
def delete_record(request: HttpRequest, pk: str) -> HttpResponse:
    record: Record = get_object_or_404(Record, id=pk)
    _record_service.delete(record)
    messages.success(request, "Registro eliminado correctamente")
    return redirect("home")


@login_required
def update_record(request: HttpRequest, pk: str) -> HttpResponse:
    current_record: Record = get_object_or_404(Record, id=pk)
    form: RecordForm = RecordForm(request.POST or None, instance=current_record)

    if form.is_valid():
        form.save()
        messages.success(request, "Registro actualizado correctamente")
        return redirect("home")

    return render(request, "update_record.html", {"form": form})
