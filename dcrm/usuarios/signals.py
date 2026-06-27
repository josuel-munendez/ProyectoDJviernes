"""Señales de la aplicación usuarios.

Crea automáticamente un perfil de usuario cuando se registra
una nueva cuenta, excepto para superusuarios.
"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un UserProfile automáticamente al registrarse un nuevo usuario."""
    if created and not instance.is_superuser:
        UserProfile.objects.get_or_create(user=instance, defaults={"_rol": UserProfile.ROL_CLIENTE})
