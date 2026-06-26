import csv

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Record


@login_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="registros.csv"'
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow(["ID", "Nombre", "Apellido", "Email", "Telefono", "Direccion", "Ciudad", "Estado", "CP"])

    for record in Record.objects.all().values_list(
        "id", "first_name", "last_name", "email", "phone", "address", "city", "state", "zip_code"
    ):
        writer.writerow(record)

    return response
