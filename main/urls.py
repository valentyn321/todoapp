from django.conf.urls import url
from django.urls import path
from . import views
from .views import TodoListView, CompletedTodoListView

urlpatterns = [
	path('', TodoListView.as_view(), name="home"),
    path('completed_todos', CompletedTodoListView.as_view(), name="completed_todos"),
	# path('add_new', views.add_new, name="add_new"),
	path('ajax/add_new', views.add_new_ajax, name="add_new_ajax"),
    # path('delete_todo/<int:todo_id>/', views.delete_todo, name="delete_todo"),
    path('ajax/delete_todo/<int:todo_id>/', views.delete_todo_ajax, name="delete_todo_ajax"),
	# path('complete_todo/<int:todo_id>/', views.complete_todo, name="complete_todo"),
	path('ajax/complete_todo/<int:todo_id>/', views.complete_todo_ajax, name="complete_todo_ajax"),
]
