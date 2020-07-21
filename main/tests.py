from django.test import TestCase, Client
from main.models import Todo, Category

class MainPageTest(TestCase):

    def setUp(self):
        client = Client()
        response = self.client.post('/register/', {'username': 'new_tester', 'email': 'new_tester@gmail.com', 'password1': 'tester123', 'password2': 'tester123'})

    def test_ajax_adds_and_complete_and_delet_items_corectly(self):        
        new_categ = Category.objects.create(title="General")
        response = self.client.post('/ajax/add_new', {'text': 'A new list item', 'categ': 1, 'date': ''})
        
        number_of_todos = Todo.objects.count()
        self.assertEqual(number_of_todos, 1)
        self.assertFalse(Todo.objects.first().status)
    
        response = self.client.post('/ajax/complete_todo/1/')
        self.assertTrue(Todo.objects.first().status)

        response = self.client.post('/ajax/delete_todo/1/')
        number_of_todos = Todo.objects.count()
        self.assertEqual(number_of_todos, 0)




