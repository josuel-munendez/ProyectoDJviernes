"""Vistas de la aplicación catálogo.

Proporciona listados de categorías y catálogos para usuarios
autenticados, y una vista pública de productos con búsqueda y filtros.
"""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.db.models import Q

from core.services import CrudService
from .models import Categoria, Catalogo
from productos.models import Producto


@login_required
def listado_categorias(request: HttpRequest) -> HttpResponse:
    """Muestra el listado de todas las categorías."""
    categorias = Categoria.objects.all()
    return render(request, "catalogo/categorias.html", {"categorias": categorias})


@login_required
def listado_catalogos(request: HttpRequest) -> HttpResponse:
    """Muestra el listado paginado de catálogos con datos relacionados."""
    catalogos = Catalogo.objects.select_related("categoria", "producto").all().order_by("-id")
    paginator = Paginator(catalogos, 5)
    page = request.GET.get("page")
    catalogos_page = paginator.get_page(page)
    return render(request, "catalogo/catalogos.html", {"catalogos": catalogos_page})


def productos_publicos(request: HttpRequest) -> HttpResponse:
    """Vista pública de productos con búsqueda y filtro por categoría.

    Permite buscar productos por nombre, descripción o código,
    y filtrar por categoría seleccionada.
    """
    query = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()
    productos = Producto.objects.all().order_by("nombre")

    # Filtro por término de búsqueda
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query) | Q(codigo__icontains=query)
        )
    # Filtro por categoría seleccionada
    if categoria_id and categoria_id.isdigit():
        cat_id = int(categoria_id)
        catalogo_ids = Catalogo.objects.filter(categoria_id=cat_id).values_list("producto_id", flat=True)
        productos = productos.filter(id__in=catalogo_ids)

    paginator = Paginator(productos, 8)
    page = request.GET.get("page")
    productos_page = paginator.get_page(page)
    categorias = Categoria.objects.all()
    return render(request, "catalogo/productos_publicos.html", {
        "productos": productos_page,
        "categorias": categorias,
        "query": query,
        "categoria_seleccionada": categoria_id,
    })
