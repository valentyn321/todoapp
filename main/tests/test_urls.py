from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import TodoListView, CompletedTodoListView, category_template


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, TodoListView)

    def test_complete_todos_url_resolves(self):
        url = reverse('completed_todos')
        self.assertEquals(resolve(url).func.view_class, CompletedTodoListView)

    def test_category_template_url_resoves(self):
        url = reverse('category_template', args=[1])
        self.assertEquals(resolve(url).func, category_template)