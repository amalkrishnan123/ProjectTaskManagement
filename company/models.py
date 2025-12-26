from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    emp_id=models.CharField(max_length=10)
    name=models.CharField(max_length=50)
    age=models.PositiveIntegerField()
    designation=models.CharField(max_length=50)
    password_change=models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    startdate=models.DateField()
    enddate=models.DateField()

    def __str__(self):
        return self.name
    
class Task(models.Model):
    STATUS_CHOICE=[
        ('pending','Pending'),
        ('in_progress','In Progress'),
        ('completed','Completed')
    ]
    PRIORITY_CHOICES=[
        ('low','Low'),
        ('medium','Medium'),
        ('high','High')
    ]
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE,default='pending')
    priority=models.CharField(max_length=50,choices=PRIORITY_CHOICES,default='medium')
    due_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    