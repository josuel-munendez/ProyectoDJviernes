from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
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
