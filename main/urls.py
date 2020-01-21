from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
    path('completed_todos', views.completed_todos, name="completed_todos"),
	path('add_new', views.add_new, name="add_new"),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name="delete_todo"),
	path('complete_todo/<int:todo_id>/', views.complete_todo, name="complete_todo"),
]
