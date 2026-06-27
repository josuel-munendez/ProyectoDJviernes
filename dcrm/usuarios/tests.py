"""Pruebas unitarias para la aplicación usuarios."""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTest(TestCase):
    """Pruebas para el modelo UserProfile."""

    def setUp(self):
        """Crea un usuario de prueba antes de cada test."""
        self.user = User.objects.create_user(username="testuser", password="pass1234")

    def test_profile_created_on_user_create(self):
        """Verifica que se cree un perfil al crear un usuario."""
        self.assertTrue(hasattr(self.user, "profile"))

    def test_default_role_is_cliente(self):
        """Verifica que el rol por defecto sea cliente."""
        profile = self.user.profile
        self.assertEqual(profile._rol, UserProfile.ROL_CLIENTE)

    def test_es_admin_returns_false_for_cliente(self):
        """Verifica que un cliente no sea administrador."""
        self.assertFalse(self.user.profile.es_admin())

    def test_es_cliente_returns_true(self):
        """Verifica que el método es_cliente retorne True."""
        self.assertTrue(self.user.profile.es_cliente())
