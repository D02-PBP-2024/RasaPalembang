from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime
import django

def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('login')
    return render(request, 'signup/index.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django.contrib.auth.login(request, user)
            response = HttpResponseRedirect('/')
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    return render(request, 'login/index.html', {'form': form})


def logout(request):
    django.contrib.auth.logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('last_login')
    return response


@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile/index.html', {})
