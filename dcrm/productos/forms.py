from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "codigo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción", "rows": 3}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Stock"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código"}),
        }
