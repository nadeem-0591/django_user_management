# user_app/urls.py

from django.urls import path
from .views import user_login, select_role, task_list, create_task

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('select_role/', select_role, name='select_role'),
    path('tasks/<str:role>/', task_list, name='task_list'),
    path('create_task/<str:role>/', create_task, name='create_task'),
]
