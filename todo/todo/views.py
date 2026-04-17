from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from todo.models import TODOO


@login_required(login_url='/loginn/')
def home(request):
    return redirect('/todopage/')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        email = request.POST.get('emailid')
        password = request.POST.get('pwd')
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('/loginn/')

    return render(request, 'signup.html')


def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')
        # authenticate() returns None if credentials are invalid
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todopage/')
        else:
            return redirect('/loginn/')

    return render(request, 'loginn.html')


@login_required(login_url='/loginn/')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        TODOO.objects.create(title=title, user=request.user)
        return redirect('/todopage/')

    todos = TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': todos})


@login_required(login_url='/loginn/')
def delete_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno, user=request.user)
    obj.delete()
    return redirect('/todopage/')


@login_required(login_url='/loginn/')
def edit_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        obj.title = title
        obj.save()
        return redirect('/todopage/')

    return render(request, 'edit_todo.html', {'obj': obj})


@login_required(login_url='/loginn/')
def toggle_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno, user=request.user)
    obj.status = not obj.status
    obj.save()
    return redirect('/todopage/')


def signout(request):
    logout(request)
    return redirect('/loginn/')
