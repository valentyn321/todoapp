from django.conf.urls import url
from django.urls import path

from django.contrib.auth.decorators import login_required

from main import views as m_views

urlpatterns = [
    path('', login_required(m_views.TodoListView.as_view()), name="home"),
    path('completed_todos', m_views.CompletedTodoListView.as_view(), name="completed_todos"),
    path('category/<int:category_id>', m_views.category_template, name="category_template"),

    path('ajax/add_new', m_views.add_new_ajax, name="add_new_ajax"),
    path('ajax/delete_todo/<int:todo_id>/', m_views.delete_todo_ajax, name="delete_todo_ajax"),
    path('ajax/complete_todo/<int:todo_id>/', m_views.complete_todo_ajax, name="complete_todo_ajax"),
]
