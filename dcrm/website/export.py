"""Exportacion de datos de la aplicacion website a formato CSV."""

import csv

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Record


@login_required
def export_csv(request):
    """Exporta todos los registros de clientes a un archivo CSV con codificacion UTF-8."""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="registros.csv"'
    # Agrega BOM para compatibilidad con Excel en Windows
    response.write("\ufeff")

    writer = csv.writer(response)
    # Escribe la fila de encabezados
    writer.writerow(["ID", "Nombre", "Apellido", "Email", "Telefono", "Direccion", "Ciudad", "Estado", "CP"])

    # Escribe los datos de cada registro como una fila
    for record in Record.objects.all().values_list(
        "id", "first_name", "last_name", "email", "phone", "address", "city", "state", "zip_code"
    ):
        writer.writerow(record)

    return response
