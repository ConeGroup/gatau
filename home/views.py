from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'homepage.html', {})

@login_required
def user_home(request):
    context = {
        'name': request.user.username,
    }
    return render(request, "homepage.html", context)

@csrf_exempt
def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('home')
            
    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
    # Check to see if someone logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse('user_home'))
            messages.success(request, "Login succeeded")
            return response
        else: 
            return HttpResponse(messages.info(request, 'Sorry, incorrect username or password. Please try again.'), status=400)

@csrf_exempt
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def show_review_page(request):
    return HttpResponseRedirect(reverse('reviews:show_main'))