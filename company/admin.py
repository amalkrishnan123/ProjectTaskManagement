from django.contrib import admin
from .models import Project,Task,Employee,TaskUpdate
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Employee)
admin.site.register(TaskUpdate)

# Register your models here.
