from django.shortcuts import render
from django.utils import timezone
from .models import Todo, Category
from .forms import TodoForm
from users.models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class TodoListView(ListView):
    model = Todo
    template_name = 'main/todo_list.html'
    context_object_name = 'todo_items'
    form = TodoForm

    def get_context_data(self, **kwargs):
        todo_items = Todo.objects.filter(status=False, user_id=self.request.user.id).order_by("deadline")[:5]
        completed_items = Todo.objects.filter(status=True, user_id=self.request.user.id).order_by("-added_date")[:5]
        category_list = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['todo_items'] = todo_items
        context['completed_items'] = completed_items
        context['category_list'] = category_list
        context['form'] = self.form
        return context
    


class CompletedTodoListView(ListView):
    model = Todo
    template_name = 'main/completed_todos.html'
    context_object_name = 'completed_todos'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Todo.objects.filter(status=True, user_id=self.request.user.id).order_by("-added_date")
        return queryset
    

    # def get_context_data(self, **kwargs):
    #     completed_todos = Todo.objects.filter(status=True, user_id=self.request.user.id).order_by("-added_date")
    #     context = super().get_context_data(**kwargs)
    #     context['completed_todos'] = completed_todos
    #     return context
    

#There are some views for ajax_requests


def add_new_ajax(request):
    current_date = timezone.now()
    content = request.POST["text"]
    category = Category.objects.get(id=request.POST["categ"])
    date = request.POST['date']
    if content != "":
        complete = False
        created_obj = Todo.objects.create(added_date=current_date, text=content, status=complete, user_id=request.user.id, category=category, deadline=date)
    else:
        messages.warning(request, f'Fill up task field!')
        
    return JsonResponse({})

def complete_todo_ajax(request, todo_id):

    completed = Todo.objects.get(id=todo_id)
    completed.status = True
    completed.save()

    user_id = request.user.id
    active_profile = Profile.objects.get(user=user_id)
    active_profile.number_of_todos += 1
    active_profile.save()
    
    data = {} 

    return JsonResponse(data)



def delete_todo_ajax(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    return JsonResponse({})


#There are some func-based views

def category_template(request, category_id):

    selected_category = Category.objects.get(id=category_id)
    todos_in_category = Todo.objects.filter(status=False, user_id=request.user.id, category=category_id).order_by("deadline")

    return render(request, 'main/category_template.html', {'selected_category': selected_category, 'todos_in_category': todos_in_category})
