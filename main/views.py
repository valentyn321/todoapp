from django.shortcuts import render
from django.utils import timezone
from .models import Todo
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse

def home_ajax(request):
    print(Profile.objects.all())
    todo_items = Todo.objects.filter(status=False, user_id=request.user.id).order_by("-added_date")
    completed_items = Todo.objects.filter(status=True, user_id=request.user.id).order_by("-added_date")[:5]
    data = {
        'todo_items': todo_items,
        'completed_items': completed_items
    } 
    return JsonResponse(data)



@login_required
def home(request):
    todo_items = Todo.objects.filter(status=False, user_id=request.user.id).order_by("-added_date")
    completed_items = Todo.objects.filter(status=True, user_id=request.user.id).order_by("-added_date")[:5] 
    return render(request, 'main/index.html', {"todo_items": todo_items, 'completed_items': completed_items})


def add_new_ajax(request):
    current_date = timezone.now()
    content = request.POST["text"]
    complete = False
    created_obj = Todo.objects.create(added_date=current_date, text=content, status=complete, user_id=request.user.id)
    
    data = {
        'is_not_null': True
    } 
    return JsonResponse(data)



# def add_new(request):
#     current_date = timezone.now()
#     content = request.POST["content"]
#     complete = False 
#     created_obj = Todo.objects.create(added_date=current_date, text=content, status=complete, user_id=request.user.id)
#     return HttpResponseRedirect("/")
  

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




# def complete_todo(request, todo_id):

#     completed = Todo.objects.get(id=todo_id)
#     completed.status = True
#     print('all right!')
#     completed.save()

#     user_id = request.user.id
#     active_profile = Profile.objects.get(user=user_id)
#     active_profile.number_of_todos += 1
#     active_profile.save()
    
#     return HttpResponseRedirect("/")


def delete_todo(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/")

@login_required
def completed_todos(request):

    completed_items = Todo.objects.filter(status=True, user_id=request.user.id).order_by("-added_date") 
    return render(request, 'main/completed_todos.html', {'completed_items': completed_items})
