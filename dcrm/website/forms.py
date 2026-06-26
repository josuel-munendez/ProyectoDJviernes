from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Record


class LoginForm(AuthenticationForm):
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


class UserRegisterForm(UserCreationForm):
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

    def __init__(self, *args, **kwargs):
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

    class Meta:
        model = Record
        fields = ["first_name", "last_name", "email", "phone", "address", "city", "state", "zip_code"]


AddRecordForm = RecordForm
