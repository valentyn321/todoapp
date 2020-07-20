from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View 
from django.views.decorators.csrf import csrf_exempt


class RegisterView(View): #class-based register view
    form = UserRegisterForm()
    template_name = 'users/register.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        profile = Profile()
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.save()
            profile.user = user
            profile.save()            
            messages.success(request, 'Account created successfully!.')
            return redirect('home')
        else:
            messages.warning(request, 'Something wrong with your data, check all info one more time :(')
            return redirect('register')
   

class ProfileView(View): #class-based view

    template_name = 'users/profile.html'


    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account has been updated successfully!')
            return redirect('profile')
        else:
            context = {
            'u_form': u_form,
            'p_form': p_form
            }
            return render(request, self.template_name, context) 
