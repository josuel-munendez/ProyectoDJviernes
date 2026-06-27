"""Pruebas unitarias para los modelos de la aplicacion website."""

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Record


class RecordModelTest(TestCase):
    """Pruebas para el modelo Record del CRM."""

    def setUp(self):
        """Crea un registro de prueba antes de cada test."""
        self.record = Record.objects.create(
            first_name="Juan",
            last_name="Perez",
            email="juan@test.com",
            phone="123456789",
            address="Calle 123",
            city="Bogota",
            state="Cundinamarca",
            zip_code="110111",
        )

    def test_record_creation(self):
        """Verifica que un registro se cree correctamente con los datos proporcionados."""
        self.assertEqual(self.record.first_name, "Juan")
        self.assertEqual(self.record.email, "juan@test.com")

    def test_record_str(self):
        """Verifica que la representacion en cadena incluya nombre y apellido."""
        self.assertIn("Juan", str(self.record))
        self.assertIn("Perez", str(self.record))

    def test_full_name(self):
        """Verifica que el metodo full_name retorne el nombre completo."""
        self.assertEqual(self.record.full_name(), "Juan Perez")

    def test_get_contact_info(self):
        """Verifica que get_contact_info retorne el email y telefono."""
        self.assertIn("juan@test.com", self.record.get_contact_info())
