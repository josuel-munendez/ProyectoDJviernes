from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.services import CrudService
from .models import Categoria, Catalogo


@login_required
def listado_categorias(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.all()
    return render(request, "catalogo/categorias.html", {"categorias": categorias})


@login_required
def listado_catalogos(request: HttpRequest) -> HttpResponse:
    catalogos = Catalogo.objects.select_related("categoria", "producto").all()
    paginator = Paginator(catalogos, 5)
    page = request.GET.get("page")
    catalogos_page = paginator.get_page(page)
    return render(request, "catalogo/catalogos.html", {"catalogos": catalogos_page})
