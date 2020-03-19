from django.conf.urls import url
from django.urls import path
from . import views
from .views import TodoListView, CompletedTodoListView

urlpatterns = [
    path('', TodoListView.as_view(), name="home"),
    path('completed_todos', CompletedTodoListView.as_view(), name="completed_todos"),
    path('category/<int:category_id>', views.category_template, name="category_template"),
    path('ajax/add_new', views.add_new_ajax, name="add_new_ajax"),
    path('ajax/delete_todo/<int:todo_id>/', views.delete_todo_ajax, name="delete_todo_ajax"),
    path('ajax/complete_todo/<int:todo_id>/', views.complete_todo_ajax, name="complete_todo_ajax"),
]
