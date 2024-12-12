from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import RegisterUserSerializer
from django.contrib.auth.hashers import check_password


class RegisterUserSerializerTest(APITestCase):
    def test_valid_registration(self):
        """Probar que el registro de usuario válido se guarda correctamente"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }


        # Crear un nuevo usuario usando el serializer
        serializer = RegisterUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())


        user = serializer.save()
        # Asegurarse de que el usuario se ha creado
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')


        # Verificar que la contraseña está correctamente hasheada
        # La contraseña debe coincidir con el hash guardado
        self.assertTrue(check_password('password123', user.password))


    def test_invalid_password(self):
        """Probar que se valida la contraseña correctamente (mínimo 8 caracteres)"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'short'
        }


        serializer = RegisterUserSerializer(data=data)
        # La contraseña corta no debería ser válida
        self.assertFalse(serializer.is_valid())
        # Debe haber un error para el campo 'password'
        self.assertIn('password', serializer.errors)


    def test_password_not_in_response(self):
        """Verificar que la contraseña no se incluye en la respuesta del serializer"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }


        serializer = RegisterUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()


        # Asegurarse de que la contraseña no aparece en la respuesta serializada
        user_data = RegisterUserSerializer(user).data
        self.assertNotIn('password', user_data)
