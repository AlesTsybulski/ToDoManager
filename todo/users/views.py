from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

# Получаем нашу кастомную модель пользователя
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        email = request.POST.get('emailid')
        password = request.POST.get('pwd')
        # Создаем пользователя через нашу новую модель
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('/loginn/')

    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todopage/')
        else:
            return redirect('/loginn/')

    return render(request, 'loginn.html')

def signout(request):
    logout(request)
    return redirect('/loginn/')