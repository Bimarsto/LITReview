from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms


def signup(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    return render(request, 'authentication/signup.html', context={'form': form})


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                message = f"Bonjour {user.username}."
                return redirect('index')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')
