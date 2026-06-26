import json
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent.parent / "fixtures" / "initial_data.json"
)

USER_PASSWORDS = {
    "admin_usu": "admin123",
    "gestor": "gestor123",
    "vendedor": "vendedor123",
    "cliente": "cliente123",
}


class Command(BaseCommand):
    help = "Load seed data from fixture and set proper passwords"

    def add_arguments(self, parser):
        parser.add_argument("--check", action="store_true", help="Check if seed data exists (exit 0 if yes, 1 if no)")

    def handle(self, *args, **options):
        if options.get("check"):
            if User.objects.filter(username__in=USER_PASSWORDS.keys()).count() == len(USER_PASSWORDS):
                self.stdout.write("Seed data already loaded.")
                return
            self.stdout.write("Seed data not loaded.")
            raise SystemExit(1)

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

            self.stdout.write("Clearing existing data...")
            CatalogoModel.objects.all().delete()
            ProductoModel.objects.all().delete()
            CategoriaModel.objects.all().delete()
            RecordModel.objects.all().delete()
            # Preserve superusers created via `createsuperuser`
            superuser_ids = list(User.objects.filter(is_superuser=True).values_list("pk", flat=True))
            UserProfileModel.objects.exclude(user_id__in=superuser_ids).delete()
            User.objects.exclude(is_superuser=True).delete()

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
                    pk_map[("auth.user", entry["pk"])] = user.pk
                    self.stdout.write(f"  Created user: {username}")

                elif model == "usuarios.userprofile":
                    old_user_pk = fields.pop("user")
                    fields["user_id"] = pk_map[("auth.user", old_user_pk)]
                    UserProfileModel.objects.update_or_create(
                        user_id=fields["user_id"], defaults=fields
                    )
                    self.stdout.write(f"  Profile for user pk={fields['user_id']}")

                elif model == "website.record":
                    obj = RecordModel.objects.create(**fields)
                    self.stdout.write(f"  Record: {fields.get('first_name', '')} {fields.get('last_name', '')}")

                elif model == "catalogo.categoria":
                    obj = CategoriaModel.objects.create(**fields)
                    pk_map[("catalogo.categoria", entry["pk"])] = obj.pk
                    self.stdout.write(f"  Category: {fields['nombre']}")

                elif model == "productos.producto":
                    obj = ProductoModel.objects.create(**fields)
                    pk_map[("productos.producto", entry["pk"])] = obj.pk
                    self.stdout.write(f"  Product: {fields['nombre']}")

                elif model == "catalogo.catalogo":
                    old_cat_pk = fields.pop("categoria")
                    old_prod_pk = fields.pop("producto")
                    fields["categoria_id"] = pk_map[("catalogo.categoria", old_cat_pk)]
                    fields["producto_id"] = pk_map[("productos.producto", old_prod_pk)]
                    CatalogoModel.objects.create(**fields)
                    self.stdout.write(f"  Catalog: {fields['nombre']}")

        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully!"))
        self.stdout.write("Users created (password in parentheses):")
        for username, pw in USER_PASSWORDS.items():
            self.stdout.write(f"  {username} ({pw})")
