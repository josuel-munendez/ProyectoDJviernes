"""Formularios de la aplicación productos.

Define el formulario para crear y editar productos con validación
de nombre mediante expresiones regulares.
"""
from django import forms
from core.validators import RegexValidator
from .models import Producto


class ProductoForm(forms.ModelForm):
    """Formulario para la creación y edición de productos."""

    def clean_nombre(self):
        """Valida que el nombre solo contenga caracteres permitidos."""
        value = self.cleaned_data.get("nombre", "")
        if value and not RegexValidator.validate("name", value):
            raise forms.ValidationError("El nombre solo puede contener letras, numeros y espacios.")
        return value

    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "codigo"]
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripcion",
            "precio": "Precio",
            "stock": "Stock",
            "codigo": "Codigo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto", "required": "", "minlength": "2"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripcion", "rows": 3}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio", "required": "", "min": "0"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Stock", "required": "", "min": "0"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Codigo", "required": ""}),
        }
