from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234")

    def test_profile_created_on_user_create(self):
        self.assertTrue(hasattr(self.user, "profile"))

    def test_default_role_is_cliente(self):
        profile = self.user.profile
        self.assertEqual(profile._rol, UserProfile.ROL_CLIENTE)

    def test_es_admin_returns_false_for_cliente(self):
        self.assertFalse(self.user.profile.es_admin())

    def test_es_cliente_returns_true(self):
        self.assertTrue(self.user.profile.es_cliente())
