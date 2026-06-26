from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http import HttpRequest


class SuperuserAdminSite(admin.AdminSite):
    def has_permission(self, request: HttpRequest) -> bool:
        return request.user.is_active and request.user.is_superuser


admin_site = SuperuserAdminSite(name="superuser_admin")

# Register auth models
from django.contrib.auth.admin import UserAdmin, GroupAdmin
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Register app models
from website.models import Record
from usuarios.models import UserProfile
from usuarios.admin import UserProfileAdmin
from productos.models import Producto
from catalogo.models import Categoria, Catalogo

admin_site.register(Record)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Producto)
admin_site.register(Categoria)
admin_site.register(Catalogo)
