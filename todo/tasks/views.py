from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task

def parse_deadline(value):
    if not value:
        return None
    return value.replace('T', ' ')

def home(request):
    if request.user.is_authenticated:
        return redirect('/todopage/')
    return render(request, 'home.html')

@login_required(login_url='/login/')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = parse_deadline(request.POST.get('deadline'))
        Task.objects.create(title=title, deadline=deadline, user=request.user)
        return redirect('/todopage/')

    todos = Task.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': todos})

@login_required(login_url='/login/')
def delete_todo(request, srno):
    if request.method == 'POST':
        obj = get_object_or_404(Task, srno=srno, user=request.user)
        obj.delete()
    return redirect('/todopage/')

@login_required(login_url='/login/')
def edit_todo(request, srno):
    obj = get_object_or_404(Task, srno=srno, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        obj.title = title
        deadline = parse_deadline(request.POST.get('deadline'))
        obj.deadline = deadline
        obj.save()
        return redirect('/todopage/')

    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url='/login/')
def toggle_todo(request, srno):
    obj = get_object_or_404(Task, srno=srno, user=request.user)
    obj.status = not obj.status
    obj.save()
    return redirect('/todopage/')