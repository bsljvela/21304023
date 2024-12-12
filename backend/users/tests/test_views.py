from rest_framework.test import APITestCase
from rest_framework import status
# from django.contrib.auth.models import User
from django.urls import reverse
from users.models import User


class UserApiViewSetTest(APITestCase):
    def setUp(self):
        # Crear un usuario administrador para probar el acceso a los endpoints protegidos
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        # Inicia sesión con el usuario administrador
        self.client.login(username='admin@example.com',
                          password='adminpassword')


        # Crear un usuario normal para pruebas
        self.normal_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword'
        )


    def test_list_users(self):
        """Probar que un administrador puede obtener la lista de usuarios"""
        url = reverse(
            'user-list')  # Asegúrate de que el nombre de la ruta coincide
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


    def test_create_user(self):
        """Probar que un administrador puede crear un usuario"""
        url = reverse('user-list')
        data = {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='new_user').count(), 1)


    def test_partial_update_user(self):
        """Probar que un administrador puede actualizar parcialmente un usuario"""
        url = reverse('user-detail', args=[self.normal_user.id])
        data = {
            'email': 'updated_email@example.com',
            'password': 'updatedpassword'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.email, 'updated_email@example.com')


    def test_access_denied_for_non_admin(self):
        """Probar que los usuarios no administradores no tienen acceso"""
        self.client.logout()
        self.client.login(username='user@example.com', password='userpassword')
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserViewTest(APITestCase):
    def setUp(self):
        # Crear un usuario normal
        self.user = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='userpassword'
        )
        self.client.login(username='user2@example.com',
                          password='userpassword')


    def test_get_authenticated_user(self):
        """Probar que un usuario autenticado puede obtener su propia información"""
        url = reverse('user-view')  # Cambia al nombre correcto de tu ruta
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user2')


class RegisterUserViewTest(APITestCase):
    def test_register_user(self):
        """Probar que se puede registrar un nuevo usuario"""
        url = reverse('register')  # Cambia al nombre correcto de tu ruta
        data = {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='new_user').count(), 1)


    def test_register_user_invalid_data(self):
        """Probar que se devuelve un error con datos inválidos"""
        url = reverse('register')
        data = {
            'username': '',
            'email': 'invalid_email',
            'password': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


