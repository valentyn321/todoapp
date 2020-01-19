from django.shortcuts import render
from django.utils import timezone
from main.models import Todo
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User

@login_required
def home(request):
    todo_items = Todo.objects.filter(status=False).order_by("-added_date")
    completed_items = Todo.objects.filter(status=True).order_by("-added_date")[:5] 
    return render(request, 'main/index.html', {"todo_items": todo_items, 'completed_items': completed_items})

def add_new(request):
    current_date = timezone.now()
    content = request.POST["content"]
    complete = False 
    created_obj = Todo.objects.create(added_date=current_date, text=content, status=complete)
    return HttpResponseRedirect("/")
    

def complete_todo(request, todo_id):

    completed = Todo.objects.get(id=todo_id)
    completed.status = True
    completed.save()

    user_id = request.user.id
    active_profile = Profile.objects.get(user=user_id)
    active_profile.number_of_todos += 1
    active_profile.save()
    
    return HttpResponseRedirect("/")


def delete_todo(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/")

