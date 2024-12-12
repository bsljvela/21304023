from django.test import TestCase
from users.models import User
from django.db import IntegrityError


class UserModelTest(TestCase):
    def setUp(self):
        """Configurar los datos iniciales para las pruebas"""
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword123"
        }
        self.user = User.objects.create_user(**self.user_data)


    def test_create_user(self):
        """Probar que un usuario puede ser creado correctamente"""
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))


    def test_email_is_unique(self):
        """Probar que el correo electrónico debe ser único"""
        with self.assertRaises(IntegrityError):  # Verificar que sea específicamente un error de integridad
            User.objects.create_user(
                email=self.user_data["email"],
                # email="anotheruser@example.com",
                username="anotheruser",
                first_name="Another",
                last_name="User2",
                password="anotherpassword123"
            )


    def test_user_string_representation(self):
        """Probar la representación en string del usuario"""
        self.assertEqual(str(self.user), self.user.email)


    def test_update_user_optional_fields(self):
        """Probar que los campos opcionales pueden ser actualizados"""
        self.user.first_name = "Updated"
        self.user.last_name = "User"
        self.user.save()


        updated_user = User.objects.get(email=self.user.email)
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "User")
