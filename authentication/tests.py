from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer, UserRegistrationSerializer


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.login_url = reverse('user_login')

    def test_user_login_success_username(self):
        # Make a POST request to the login endpoint with username
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data, format='json')
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the response contains the 'access' and 'refresh' tokens
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_success_email(self):
        # Make a POST request to the login endpoint with email
        data = {'username': self.email, 'password': self.password}
        response = self.client.post(self.login_url, data, format='json')
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the response contains the 'access' and 'refresh' tokens
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        # Make a POST request to the login endpoint with invalid credentials
        data = {'username': 'invaliduser', 'password': 'invalidpassword'}
        response = self.client.post(self.login_url, data, format='json')

        # Assert that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert that the response contains the error message 'Invalid credentials'
        self.assertEqual(str(response.data['detail']), 'Invalid credentials')

    def test_user_login_missing_username(self):
        # Make a POST request to the login endpoint without providing a username
        data = {'password': self.password}
        response = self.client.post(self.login_url, data, format='json')

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that the 'username' key is in the response data
        self.assertIn('username', response.data)

    def test_user_login_missing_password(self):
        # Make a POST request to the login endpoint without providing a password
        data = {'username': self.username}
        response = self.client.post(self.login_url, data, format='json')

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that the 'password' key is in the response data
        self.assertIn('password', response.data)


class UserLogoutTestCase(APITestCase):
    
    def test_user_logout(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Authenticate the user
        self.client.login(username='testuser', password='testpassword')

        # Make a POST request to the logout endpoint
        url = reverse('user_logout')
        response = self.client.post(url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the response contains the message 'Logout successful'
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_user_logout_unauthenticated(self):
        # Make a POST request to the logout endpoint without authenticating the user
        url = reverse('user_logout')
        response = self.client.post(url)

        # Assert that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert that the response data does not contain the 'detail' key
        self.assertEqual(response.data['message'], 'Unauthorized')


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user_register')

    def register_user(self, data):
        return self.client.post(self.register_url, data, format='json')

    def test_user_registration_success(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword', 'confirm_password': 'testpassword'}
        response = self.register_user(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Registration successful')

    def test_user_registration_invalid_data(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword', 'confirm_password': 'invalidpassword'}
        response = self.register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)

    def test_user_registration_existing_username(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        data = {'username': 'testuser', 'email': 'test2@example.com', 'password': 'testpassword', 'confirm_password': 'testpassword'}
        response = self.register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_user_registration_existing_email(self):
        User.objects.create_user(username='testuser2', email='test@example.com', password='testpassword')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword', 'confirm_password': 'testpassword'}
        response = self.register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_weak_password(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'weak', 'confirm_password': 'weak'}
        response = self.register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_mismatched_passwords(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword', 'confirm_password': 'mismatchedpassword'}
        response = self.register_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)
