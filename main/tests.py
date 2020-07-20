from django.test import TestCase, Client

class MainPageTest(TestCase):

    def setUp(self):
        client = Client()

    def test_view_redirect_to_login_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed('login.html')

    