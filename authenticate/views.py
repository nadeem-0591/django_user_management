# user_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserType, Task
import datetime
from datetime import datetime as dt


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Associate the user with a UserType entry based on their role
            user_type, created = UserType.objects.get_or_create(user=user, role='supervisor')

            return redirect('select_role')

    return render(request, 'authenticate/login.html')

@login_required
def select_role(request):
    user_types = UserType.objects.filter(user=request.user)
    print(user_types)  # Add this line for debugging

    return render(request, 'authenticate/select_role.html', {'user_types': user_types})


@login_required
def task_list(request, role):
    user_type = UserType.objects.get(user=request.user, role=role)
    tasks = Task.objects.filter(user_type=user_type)
    return render(request, 'authenticate/task_list.html', {'tasks': tasks, 'role': role})

@login_required
def create_task(request, role):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to_username = request.POST['assigned_to']
        due_date_str = request.POST['due_date']  # Add this line to get the due date string

        assigned_to = User.objects.get(username=assigned_to_username)
        user_type = UserType.objects.get(user=request.user, role=role)

        # Parse the due date string into a Python datetime object
        due_date = dt.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            user_type=user_type,
            due_date=due_date  # Add this line for the due date
        )

        return redirect('task_list', role=role)

    users = User.objects.all()
    return render(request, 'authenticate/create_task.html', {'users': users, 'role': role})
