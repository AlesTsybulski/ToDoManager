from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('fnm', '').strip()
        email = request.POST.get('emailid', '').strip()
        password = request.POST.get('pwd', '')

        error = None
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'

        if error:
            return render(request, 'signup.html', {'error': error, 'fnm': username, 'emailid': email})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('/login/')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todopage/')
        else:
            return redirect('/login/')

    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('/login/')
