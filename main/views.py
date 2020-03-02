from django.shortcuts import render
from django.utils import timezone
from .models import Todo
from users.models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class TodoListView(ListView):
    model = Todo
    template_name = 'main/todo_list.html'
    


    # def get_queryset(self):
    #     qs = super().get_queryset() 
    #     uncomleted_todos = qs.filter(status=False).order_by("-added_date")
    #     completed_todos = qs.filter(status=True).order_by("-added_date")
    #     return uncomleted_todos, completed_todos


    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        todo_items = Todo.objects.filter(status=False, user_id=request.user.id).order_by("-added_date")
        completed_items = Todo.objects.filter(status=True, user_id=request.user.id).order_by("-added_date")[:5]
        return render(request, self.template_name, {"todo_items": todo_items, 'completed_items': completed_items})


class CompletedTodoListView(ListView):
    model = Todo
    template_name = 'main/completed_todos.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        completed_items = Todo.objects.filter(status=True, user_id=request.user.id).order_by("-added_date") 
        return render(request, self.template_name, {'completed_items': completed_items})




def home_ajax(request):
    todo_items = Todo.objects.filter(status=False, user_id=request.user.id).order_by("-added_date")
    completed_items = Todo.objects.filter(status=True, user_id=request.user.id).order_by("-added_date")[:5]
    data = {
        'todo_items': todo_items,
        'completed_items': completed_items
    } 
    return JsonResponse(data)

def add_new_ajax(request):
    current_date = timezone.now()
    content = request.POST["text"]
    complete = False
    created_obj = Todo.objects.create(added_date=current_date, text=content, status=complete, user_id=request.user.id)
    
    data = {
        'is_not_null': True
    } 
    return JsonResponse(data)

def complete_todo_ajax(request, todo_id):

    completed = Todo.objects.get(id=todo_id)
    completed.status = True
    completed.save()

    user_id = request.user.id
    active_profile = Profile.objects.get(user=user_id)
    active_profile.number_of_todos += 1
    active_profile.save()
    
    data = {
        'if_success': "Todo_completed!"
    } 

    return JsonResponse(data)



def delete_todo_ajax(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    return JsonResponse({})




