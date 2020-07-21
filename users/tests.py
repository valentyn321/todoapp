from django.test import TestCase, Client 
from django.contrib.auth import get_user_model, authenticate, get_user
import json

from users.models import Profile


class RegisterNewUserAndLogInTest(TestCase):

    def setUp(self):
        client = Client()
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def test_register_url(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.resolver_match.view_name, 'register')

    def test_sign_up_and_redirects_correctly(self):
        response = self.client.post('/register/', {'username': 'new_tester', 'email': 'new_tester@gmail.com', 'password1': 'tester123', 'password2': 'tester123'})
        number_of_profiles = Profile.objects.count()
        self.assertEqual(number_of_profiles, 1)
        self.assertRedirects(response, f'/')

    def test_sign_up_incoreect_password(self):
        response = self.client.post('/register/', {'username': 'new_tester', 'email': 'new_tester@gmail.com', 'password1': 'tester123', 'password2': 'tester1234'})
        self.assertRedirects(response, f'/register/')

    def test_sign_up_incoreect_email(self):
        response = self.client.post('/register/', {'username': 'new_tester', 'email': 'new_tester@gmailcom', 'password1': 'tester123', 'password2': 'tester1234'})
        self.assertRedirects(response, f'/register/')
        

    def test_login_url(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEqual(response.resolver_match.view_name, 'login') 

    
    def test_log_in_and_redirects_correctly(self):
        response = self.client.post('/login/', {'username': 'test', 'password': '12test12'})
        self.assertRedirects(response, f'/')

    def test_wrong_username(self):
        response = self.client.post('/login/', {'username': 'wrong', 'password': '12test12'})
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_wrong_password(self):
        response = self.client.post('/login/', {'username': 'wrong', 'password': 'wrong'})
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

