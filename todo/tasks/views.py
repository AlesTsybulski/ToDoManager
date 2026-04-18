from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task 

@login_required(login_url='/loginn/')
def home(request):
    return redirect('/todopage/')

@login_required(login_url='/loginn/')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        Task.objects.create(title=title, deadline=deadline, user=request.user)
        return redirect('/todopage/')

    todos = Task.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': todos})

@login_required(login_url='/loginn/')
def delete_todo(request, srno):
    if request.method == 'POST':
        obj = get_object_or_404(Task, srno=srno, user=request.user)
        obj.delete()
    return redirect('/todopage/')

@login_required(login_url='/loginn/')
def edit_todo(request, srno):
    obj = get_object_or_404(Task, srno=srno, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        obj.title = title
        deadline = request.POST.get('deadline')
        obj.deadline = deadline
        obj.save()
        return redirect('/todopage/')

    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url='/loginn/')
def toggle_todo(request, srno):
    obj = get_object_or_404(Task, srno=srno, user=request.user)
    obj.status = not obj.status
    obj.save()
    return redirect('/todopage/')