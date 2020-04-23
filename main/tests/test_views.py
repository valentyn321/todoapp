from django.test import TestCase, Client
from django.urls import reverse
from main.models import Category, Todo
import json


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.completed_todos_url = reverse('completed_todos')
        self.category_template_url = reverse('category_template', args=[1])
        Category.objects.create(
            id=1,
            title="TestingCategory"
            )


    def test_TodoListView_category_template_view_GET(self):
        
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/todo_list.html')

    def test_CompletedTodoListView_category_template_view_GET(self):
        
        response = self.client.get(self.completed_todos_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/completed_todos.html')

    def test_category_template_view_GET(self):

        response = self.client.get(self.category_template_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/category_template.html')
