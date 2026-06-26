from django.contrib.auth.models import User
from django.test import TestCase

from .models import Record


class RecordModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.record.first_name, "Juan")
        self.assertEqual(self.record.email, "juan@test.com")

    def test_record_str(self):
        self.assertIn("Juan", str(self.record))
        self.assertIn("Perez", str(self.record))

    def test_full_name(self):
        self.assertEqual(self.record.full_name(), "Juan Perez")

    def test_get_contact_info(self):
        self.assertIn("juan@test.com", self.record.get_contact_info())
