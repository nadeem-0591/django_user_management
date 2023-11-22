# authenticate/models.py

from django.contrib.auth.models import User
from django.db import models

class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('manager', 'Manager'), ('supervisor', 'Supervisor')])

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)  # Updated this line
    # Add other fields as needed

    def __str__(self):
        return self.title
