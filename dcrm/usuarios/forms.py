"""Formularios de la aplicación usuarios.

Define el formulario de registro con validación de campos
y creación automática del perfil de usuario.
"""
from django import forms
from django.contrib.auth.models import User

from core.validators import RegexValidator
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    """Formulario de registro de nuevos usuarios.

    Incluye campos de contraseña, confirmación y datos opcionales
    de contacto. Crea automáticamente el perfil asociado al usuario.
    """

    password = forms.CharField(
        label="Contrasena",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ingresa tu contrasena"}),
    )
    confirm_password = forms.CharField(
        label="Confirmar contrasena",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repite tu contrasena"}),
    )
    _telefono = forms.CharField(
        label="Telefono",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Opcional"}),
    )
    _direccion = forms.CharField(
        label="Direccion",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Opcional"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        """Asigna clases CSS y placeholders a los campos del formulario."""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name not in ("password", "confirm_password", "_telefono", "_direccion"):
                self.fields[field_name].widget.attrs["class"] = "form-control"
                placeholder_map = {
                    "username": "Nombre de usuario",
                    "email": "Correo electronico",
                    "first_name": "Nombre",
                    "last_name": "Apellido",
                }
                self.fields[field_name].widget.attrs["placeholder"] = placeholder_map.get(field_name, "")

    def clean_username(self):
        """Valida que el nombre de usuario cumpla con el formato permitido."""
        value = self.cleaned_data.get("username", "")
        if value and not RegexValidator.validate("username", value):
            raise forms.ValidationError("El usuario solo puede contener letras, numeros y @/./+/-/_.")
        return value

    def clean_password(self):
        """Valida que la contraseña cumpla los requisitos de seguridad."""
        value = self.cleaned_data.get("password", "")
        if value and not RegexValidator.validate("password", value):
            raise forms.ValidationError("La contrasena debe tener al menos 8 caracteres, incluyendo letras y numeros.")
        return value

    def clean(self):
        """Verifica que las contraseñas ingresadas coincidan."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Las contrasenas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        """Guarda el usuario con contraseña hasheada y crea su perfil."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Crea el perfil con rol de cliente por defecto
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "_rol": UserProfile.ROL_CLIENTE,
                    "_telefono": self.cleaned_data.get("_telefono", ""),
                    "_direccion": self.cleaned_data.get("_direccion", ""),
                },
            )
        return user
