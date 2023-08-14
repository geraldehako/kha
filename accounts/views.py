from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth import authenticate

# Create your views here.
# AUTHENTIFICATION--------------------------------------------------------------------------------------------
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.user.role == 'ADMINISTRATEUR':
                return redirect('menu')
            elif request.user.role == 'ACTIONNAIRE':
                return redirect('menuact')
            elif request.user.role == 'AGENT':
                return redirect('courbe_transactions')
            elif request.user.role == 'ADMINISTRATEURSUPER':
                return redirect('menu')

    return render(request,'Pages/Log/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')