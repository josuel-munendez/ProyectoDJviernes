"""Vistas de la aplicacion website del CRM.

Define las vistas para la autenticacion de usuarios,
gestion de registros de clientes (CRUD), busqueda,
administracion y exportacion de datos.
"""

from typing import Any
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from core.security import has_admin_role, log_delete, log_failed_login
from core.services import CrudService
from core.validators import RegexValidator
from .forms import AddRecordForm, LoginForm, RecordForm, UserRegisterForm
from .models import Record
from productos.models import Producto
from catalogo.models import Categoria
from django.contrib.auth.models import User
from usuarios.models import UserProfile


# Servicio generico CRUD para el modelo Record
_record_service = CrudService(Record)


def home(request: HttpRequest) -> HttpResponse:
    """Vista principal: landing page para usuarios no autenticados o listado paginado de registros."""
    # Muestra landing page si el usuario no ha iniciado sesion
    if not request.user.is_authenticated and request.method == "GET":
        return render(request, "landing.html")

    # Pagina los registros de clientes, 5 por pagina
    records_queryset: QuerySet = _record_service.get_all().order_by("-id")
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
        log_failed_login(request, request.POST.get("username", "desconocido"))
        messages.error(request, "Las credenciales no son validas")

    return render(request, "home.html", {"records": records_page})


def login_user(request: HttpRequest) -> HttpResponse:
    """Vista de inicio de sesion. Valida credenciales y autentica al usuario."""
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
    """Cierra la sesion del usuario y redirige a la pagina principal."""
    logout(request)
    messages.success(request, "Cerraste la sesion correctamente")
    return redirect("home")


@login_required
def register_user(request: HttpRequest) -> HttpResponse:
    """Vista de registro de nuevo usuario. Valida username, password y crea el usuario."""
    if request.method == "POST":
        form: UserRegisterForm = UserRegisterForm(request.POST)

        if form.is_valid():
            # Valida el nombre de usuario con expresion regular
            username: str = form.cleaned_data["username"]
            if not RegexValidator.validate("username", username):
                messages.error(request, "El nombre de usuario contiene caracteres no permitidos")
                return render(request, "register.html", {"form": form})

            # Valida la contrasena con los requisitos de seguridad
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
    """Muestra el detalle de un registro de cliente por su ID."""
    customer_record: Record = get_object_or_404(Record, id=pk)
    return render(request, "record.html", {"customer_record": customer_record})


@login_required
def delete_record(request: HttpRequest, pk: str) -> HttpResponse:
    """Elimina un registro de cliente. Solo disponible para usuarios con rol de administrador."""
    if not has_admin_role(request.user):
        messages.error(request, "No tienes permisos para eliminar registros")
        return redirect("home")
    record: Record = get_object_or_404(Record, id=pk)
    log_delete(request, "Record", record.id)
    _record_service.delete(record)
    messages.success(request, "Registro eliminado correctamente")
    return redirect("home")


@login_required
def update_record(request: HttpRequest, pk: str) -> HttpResponse:
    """Actualiza los datos de un registro de cliente existente."""
    current_record: Record = get_object_or_404(Record, id=pk)
    form: RecordForm = RecordForm(request.POST or None, instance=current_record)

    if form.is_valid():
        form.save()
        messages.success(request, "Registro actualizado correctamente")
        return redirect("home")

    return render(request, "update_record.html", {"form": form})


@login_required
def search_records(request: HttpRequest) -> HttpResponse:
    """Busca registros de clientes por nombre, apellido, email o telefono."""
    # Obtiene el termino de busqueda desde la query string
    query = request.GET.get("q", "").strip()
    results = Record.objects.none()
    if query:
        # Filtra por coincidencia parcial en nombre, apellido, email o telefono
        results = Record.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
        )
    return render(request, "search.html", {"results": results, "query": query})


@login_required
def add_record(request: HttpRequest) -> HttpResponse:
    """Crea un nuevo registro de cliente en el sistema."""
    form: AddRecordForm = AddRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Registro creado exitosamente")
        return redirect("home")
    return render(request, "add_record.html", {"form": form})


@login_required
def user_list(request: HttpRequest) -> HttpResponse:
    """Lista todos los usuarios del sistema. Solo para administradores."""
    if not has_admin_role(request.user):
        messages.error(request, "No tienes permisos para ver esta pagina")
        return redirect("home")
    users = User.objects.all().order_by("username")
    # Asegura que cada usuario tenga un perfil asociado
    for u in users:
        UserProfile.objects.get_or_create(user=u)
    return render(request, "user_list.html", {"users": users})


@login_required
def change_password(request: HttpRequest) -> HttpResponse:
    """Permite al usuario autenticado cambiar su contrasena."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contrasena cambiada exitosamente")
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


def handler404(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """Manejador personalizado para errores 404 (pagina no encontrada)."""
    return render(request, "404.html", status=404)


def handler500(request: HttpRequest) -> HttpResponse:
    """Manejador personalizado para errores 500 (error interno del servidor)."""
    return render(request, "500.html", status=500)


@login_required
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    """Panel de administracion con estadisticas del sistema. Solo para administradores."""
    if not has_admin_role(request.user):
        messages.error(request, "No tienes permisos de administrador")
        return redirect("home")
    # Recopila estadisticas generales del sistema para el dashboard
    context = {
        "total_usuarios": User.objects.count(),
        "total_clientes": Record.objects.count(),
        "total_productos": Producto.objects.count(),
        "total_categorias": Categoria.objects.count(),
    }
    return render(request, "admin_dashboard.html", context)
