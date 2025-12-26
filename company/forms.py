from django.forms import ModelForm
from .models import Project,Task,Employee
from django import forms
from django.contrib.auth.models import User
from datetime import date

class EmployeeForm(ModelForm):
    email=forms.EmailField()
    class Meta:
        model=Employee
        exclude=('user','password_change','emp_id','is_first_login')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.user.email

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields='__all__'
        widgets={
            'startdate':forms.DateInput(attrs={'class':'form-control','type':'date','min':date.today().isoformat()}),
            'enddate':forms.DateInput(attrs={'class':'form-control','type':'date','min':date.today().isoformat()})

        }

class TaskForm(ModelForm):
    class Meta:
        model=Task
        fields='__all__'
        widgets={
            'due_date':forms.DateInput(attrs={'class':'form-control','type':'date','min':date.today().isoformat()}),
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].queryset=User.objects.filter(is_staff=False)

class User_Update(ModelForm):
    email = forms.EmailField()
    class Meta:
        model=Employee
        fields='__all__'
        exclude=('is_first_login','password_change','user')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].disabled = True
        self.fields['emp_id'].disabled = True

        if self.instance.pk:
            self.fields['email'].initial = self.instance.user.email