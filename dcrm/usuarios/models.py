from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROL_CLIENTE = "cliente"
    ROL_VENDEDOR = "vendedor"
    ROL_GESTOR = "gestor"
    ROL_ADMIN = "admin"

    ROL_CHOICES = [
        (ROL_CLIENTE, "Cliente"),
        (ROL_VENDEDOR, "Vendedor"),
        (ROL_GESTOR, "Gestor"),
        (ROL_ADMIN, "Administrador"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    _rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default=ROL_CLIENTE,
        db_column="rol",
    )
    _telefono = models.CharField(max_length=15, blank=True, null=True, db_column="telefono")
    _direccion = models.CharField(max_length=255, blank=True, null=True, db_column="direccion")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

    @property
    def rol(self):
        return self._rol

    def get_rol_display(self):
        return dict(self.ROL_CHOICES).get(self._rol, self._rol)

    def es_admin(self):
        return self._rol == self.ROL_ADMIN

    def es_vendedor(self):
        return self._rol == self.ROL_VENDEDOR

    def es_gestor(self):
        return self._rol == self.ROL_GESTOR

    def es_cliente(self):
        return self._rol == self.ROL_CLIENTE
