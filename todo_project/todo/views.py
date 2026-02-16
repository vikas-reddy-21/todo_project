from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Todo
from .forms import TodoForm
from django.contrib.auth.decorators import login_required

# ---------- AUTH ----------

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('todo_list')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('todo_list')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# ---------- TODO ----------

@login_required(login_url='login')
def todo_list(request):
    todos = Todo.objects.filter(user=request.user).order_by('is_completed', 'deadline')

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()

    return render(request, 'todo_list.html', {
        'todos': todos,
        'form': form
    })


@login_required
def toggle_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('todo_list')


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo_list')

# ---------- DELETE ACCOUNT ----------

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)

        if user:
            request.user.delete()
            return redirect('login')

        return render(request, 'delete_account.html', {
            'error': 'Incorrect password'
        })

    return render(request, 'delete_account.html')

@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)

    return render(request, 'edit_todo.html', {
        'form': form
    })
