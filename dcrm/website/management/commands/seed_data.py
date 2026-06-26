import json
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent.parent / "fixtures" / "initial_data.json"
)

USER_PASSWORDS = {
    "admin": "admin123",
    "gestor": "gestor123",
    "vendedor": "vendedor123",
    "cliente": "cliente123",
}


class Command(BaseCommand):
    help = "Load seed data from fixture and set proper passwords"

    def handle(self, *args, **options):
        if not FIXTURE_PATH.exists():
            self.stderr.write(f"Fixture not found: {FIXTURE_PATH}")
            return

        with open(FIXTURE_PATH) as f:
            data = json.load(f)

        with transaction.atomic():
            from catalogo.models import Catalogo as CatalogoModel, Categoria as CategoriaModel
            from productos.models import Producto as ProductoModel
            from usuarios.models import UserProfile as UserProfileModel
            from website.models import Record as RecordModel

            # Clear in FK-safe order
            self.stdout.write("Clearing existing data...")
            CatalogoModel.objects.all().delete()
            ProductoModel.objects.all().delete()
            CategoriaModel.objects.all().delete()
            RecordModel.objects.all().delete()
            UserProfileModel.objects.all().delete()
            User.objects.all().delete()

            pk_map = {}

            for entry in data:
                model = entry["model"]
                fields = dict(entry["fields"])

                if model == "auth.user":
                    username = fields.pop("username")
                    password = fields.pop("password")
                    fields.pop("groups", None)
                    fields.pop("user_permissions", None)
                    fields.pop("last_login", None)
                    user = User.objects.create_user(
                        username=username,
                        password=USER_PASSWORDS.get(username, password),
                        **fields,
                    )
                    pk_map[entry["pk"]] = user.pk
                    self.stdout.write(f"  Created user: {username}")

                elif model == "usuarios.userprofile":
                    user_pk = pk_map[fields.pop("user")]
                    profile, created = UserProfileModel.objects.update_or_create(
                        user_id=user_pk, defaults=fields
                    )
                    self.stdout.write(f"  Profile for user pk={user_pk}")

                elif model == "website.record":
                    RecordModel.objects.create(**fields)
                    self.stdout.write(f"  Record: {fields.get('first_name', '')} {fields.get('last_name', '')}")

                elif model == "catalogo.categoria":
                    CategoriaModel.objects.create(**fields)
                    self.stdout.write(f"  Category: {fields['nombre']}")

                elif model == "productos.producto":
                    ProductoModel.objects.create(**fields)
                    self.stdout.write(f"  Product: {fields['nombre']}")

                elif model == "catalogo.catalogo":
                    fields["categoria"] = CategoriaModel.objects.get(pk=fields["categoria"])
                    fields["producto"] = ProductoModel.objects.get(pk=fields["producto"])
                    CatalogoModel.objects.create(**fields)
                    self.stdout.write(f"  Catalog: {fields['nombre']}")

        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully!"))
        self.stdout.write("Users created (password in parentheses):")
        for username, pw in USER_PASSWORDS.items():
            self.stdout.write(f"  {username} ({pw})")
