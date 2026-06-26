from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contrasena")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar contrasena")
    _telefono = forms.CharField(required=False, label="Telefono")
    _direccion = forms.CharField(required=False, label="Direccion")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Las contrasenas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "_rol": UserProfile.ROL_CLIENTE,
                    "_telefono": self.cleaned_data.get("_telefono", ""),
                    "_direccion": self.cleaned_data.get("_direccion", ""),
                },
            )
        return user
