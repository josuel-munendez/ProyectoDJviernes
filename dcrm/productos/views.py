from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Page, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.services import CrudService
from .models import Producto
from .forms import ProductoForm


_producto_service = CrudService(Producto)


@login_required
def listado(request: HttpRequest) -> HttpResponse:
    productos = _producto_service.get_all()
    paginator = Paginator(productos, 5)
    page = request.GET.get("page")
    productos_page = paginator.get_page(page)
    return render(request, "productos/listado.html", {"productos": productos_page})


@login_required
def detalle(request: HttpRequest, pk: Any) -> HttpResponse:
    producto = get_object_or_404(Producto, id=pk)
    return render(request, "productos/detalle.html", {"producto": producto})


@login_required
def crear(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente")
            return redirect("productos:listado")
    else:
        form = ProductoForm()
    return render(request, "productos/form.html", {"form": form, "titulo": "Crear Producto"})


@login_required
def editar(request: HttpRequest, pk: Any) -> HttpResponse:
    producto = get_object_or_404(Producto, id=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente")
            return redirect("productos:listado")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "productos/form.html", {"form": form, "titulo": "Editar Producto"})


@login_required
def eliminar(request: HttpRequest, pk: Any) -> HttpResponse:
    producto = get_object_or_404(Producto, id=pk)
    _producto_service.delete(producto)
    messages.success(request, "Producto eliminado exitosamente")
    return redirect("productos:listado")
