"""Formularios de la aplicacion website.

Define los formularios para autenticacion, registro de
usuarios y gestion de registros de clientes.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from core.validators import RegexValidator
from .models import Record


class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesion con validacion de nombre de usuario."""
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre de usuario",
            "class": "form-control",
            "required": "",
            "autocomplete": "username",
            "minlength": "3",
        })
    )
    password = forms.CharField(
        label="Contrasena",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contrasena",
            "class": "form-control",
            "required": "",
            "autocomplete": "current-password",
            "minlength": "8",
        })
    )

    def clean_username(self):
        """Valida que el nombre de usuario cumpla con el formato permitido."""
        value = self.cleaned_data.get("username", "")
        if value and not RegexValidator.validate("username", value):
            raise forms.ValidationError("El usuario solo puede contener letras, numeros y @/./+/-/_.")
        return value


class UserRegisterForm(UserCreationForm):
    """Formulario de registro de nuevo usuario con campos adicionales de perfil."""
    email = forms.EmailField(
        label="Correo electronico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electronico"}),
    )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_first_name(self):
        """Valida que el nombre solo contenga letras y espacios."""
        value = self.cleaned_data.get("first_name", "")
        if value and not RegexValidator.validate("name", value):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def clean_last_name(self):
        """Valida que el apellido solo contenga letras y espacios."""
        value = self.cleaned_data.get("last_name", "")
        if value and not RegexValidator.validate("name", value):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        return value

    def clean_email(self):
        """Valida que el correo electronico tenga un formato valido."""
        value = self.cleaned_data.get("email", "")
        if value and not RegexValidator.validate("email", value):
            raise forms.ValidationError("El formato del email no es valido.")
        return value

    def __init__(self, *args, **kwargs):
        """Inicializa el formulario asignando clases y atributos Bootstrap a los campos."""
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Nombre de usuario"
        self.fields["username"].label = "Usuario"
        self.fields["username"].help_text = (
            '<span class="form-text text-muted">Requerido. 150 caracteres o menos. '
            "Letras, digitos y @/./+/-/_ solamente.</span>"
        )

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Contrasena"
        self.fields["password1"].label = "Contrasena"
        self.fields["password1"].help_text = (
            '<ul class="form-text text-muted">'
            "<li>Tu contrasena no puede ser demasiado similar a tu otra informacion personal.</li>"
            "<li>Tu contrasena debe contener al menos 8 caracteres.</li>"
            "<li>Tu contrasena no puede ser una contrasena comun.</li>"
            "<li>Tu contrasena no puede ser completamente numerica.</li>"
            "</ul>"
        )

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirmar contrasena"
        self.fields["password2"].label = "Confirmar contrasena"
        self.fields["password2"].help_text = (
            '<span class="form-text text-muted">Requerido. Debe coincidir con la contrasena anterior.</span>'
        )


class RecordForm(forms.ModelForm):
    """Formulario para crear y actualizar registros de clientes."""
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control", "required": "", "minlength": "2"}),
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"placeholder": "Apellido", "class": "form-control", "required": "", "minlength": "2"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control", "required": ""}),
    )
    phone = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={"placeholder": "Telefono", "class": "form-control", "required": "", "minlength": "7"}),
    )
    address = forms.CharField(
        label="Direccion",
        widget=forms.TextInput(attrs={"placeholder": "Direccion", "class": "form-control", "required": ""}),
    )
    city = forms.CharField(
        label="Ciudad",
        widget=forms.TextInput(attrs={"placeholder": "Ciudad", "class": "form-control", "required": ""}),
    )
    state = forms.CharField(
        label="Estado",
        widget=forms.TextInput(attrs={"placeholder": "Estado", "class": "form-control", "required": ""}),
    )
    zip_code = forms.CharField(
        label="Codigo Postal",
        widget=forms.TextInput(attrs={"placeholder": "Codigo Postal", "class": "form-control", "required": "", "minlength": "4"}),
    )

    def clean_first_name(self):
        """Valida que el nombre solo contenga letras y espacios."""
        value = self.cleaned_data.get("first_name", "")
        if value and not RegexValidator.validate("name", value):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def clean_last_name(self):
        """Valida que el apellido solo contenga letras y espacios."""
        value = self.cleaned_data.get("last_name", "")
        if value and not RegexValidator.validate("name", value):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        return value

    def clean_email(self):
        """Valida que el correo electronico tenga un formato valido."""
        value = self.cleaned_data.get("email", "")
        if value and not RegexValidator.validate("email", value):
            raise forms.ValidationError("El formato del email no es valido.")
        return value

    def clean_phone(self):
        """Valida que el telefono tenga entre 7 y 15 digitos, con signo + opcional."""
        value = self.cleaned_data.get("phone", "")
        if value and not RegexValidator.validate("phone", value):
            raise forms.ValidationError("El telefono debe contener entre 7 y 15 digitos, opcionalmente con + al inicio.")
        return value

    def clean_zip_code(self):
        """Valida que el codigo postal tenga entre 4 y 10 digitos."""
        value = self.cleaned_data.get("zip_code", "")
        if value and not RegexValidator.validate("zip_code", value):
            raise forms.ValidationError("El codigo postal debe contener entre 4 y 10 digitos.")
        return value

    class Meta:
        model = Record
        fields = ["first_name", "last_name", "email", "phone", "address", "city", "state", "zip_code"]


# Alias para mantener compatibilidad con importaciones existentes
AddRecordForm = RecordForm
