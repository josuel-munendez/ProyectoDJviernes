"""Modelos de la aplicación usuarios.

Define el perfil extendido de usuario con roles y datos de contacto.
"""
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Perfil extendido del usuario de Django.

    Almacena el rol, teléfono y dirección asociados a cada cuenta de usuario.
    """

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
        """Representación en cadena del perfil."""
        return f"{self.user.username} - {self.get_rol_display()}"

    @property
    def rol(self):
        """Retorna el rol del usuario."""
        return self._rol

    @property
    def telefono(self):
        """Retorna el teléfono del usuario."""
        return self._telefono

    @telefono.setter
    def telefono(self, value):
        """Establece el teléfono del usuario."""
        self._telefono = value

    @property
    def direccion(self):
        """Retorna la dirección del usuario."""
        return self._direccion

    @direccion.setter
    def direccion(self, value):
        """Establece la dirección del usuario."""
        self._direccion = value

    def get_rol_display(self):
        """Retorna el nombre legible del rol actual."""
        return dict(self.ROL_CHOICES).get(self._rol, self._rol)

    def es_admin(self):
        """Verifica si el usuario tiene rol de administrador."""
        return self._rol == self.ROL_ADMIN

    def es_vendedor(self):
        """Verifica si el usuario tiene rol de vendedor."""
        return self._rol == self.ROL_VENDEDOR

    def es_gestor(self):
        """Verifica si el usuario tiene rol de gestor."""
        return self._rol == self.ROL_GESTOR

    def es_cliente(self):
        """Verifica si el usuario tiene rol de cliente."""
        return self._rol == self.ROL_CLIENTE
