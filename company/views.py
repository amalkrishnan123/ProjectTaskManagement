from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProjectForm,TaskForm,EmployeeForm,User_Update
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .models import Project,Task,Employee
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random,string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def generate_password(length=8):
    return get_random_string(length)

def generate_emp_id(length=3):
    emp_id=string.digits
    return f"EMP{''.join(random.choice(emp_id) for _ in range(length))}"

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.get(username=username)
        if not user_obj.is_active:
            messages.error(request,'Your account has been blocked. Please contact the admin.')
            return render(request, 'home.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_home')
            elif user.employee.is_first_login:
                return redirect('force_change_credentials')
            elif user.is_active and not user.is_staff:
                    return redirect('userpage')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'home.html')

@login_required
def admin_home_page(request):
    if not request.user.is_staff:
        return redirect('home')
    project=Project.objects.all()
    task=Task.objects.all()
    task_count=task.count()
    pro_count=project.count()
    context={
        'pro_count':pro_count,
        'task_count':task_count
    }
    return render(request,'admin_home_page.html',context)

@login_required
def userpage(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    t_count = tasks.count()
    p_count = tasks.values_list('project', flat=True).distinct().count()
    completed=tasks.filter(status='completed').count()
    pending=tasks.filter(status='pending').count()
    in_progress=tasks.filter(status='in_progress').count()
    context={'completed':completed,
             'pending':pending,
             'in_progress':in_progress,
             't_count': t_count,
             'p_count': p_count,
             'tsk': tasks
             }
    return render(request, 'userpage.html',context)

@login_required
def project_create_page(request):
        if not request.user.is_staff:
            return redirect('home')
        if request.method=='POST':
            form=ProjectForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('prolist')
        else:
            form=ProjectForm()
        return render(request,'project_create.html',{'form':form,'save':'create'})

@login_required
def editproject(request,id):
    if not request.user.is_staff:
        return redirect('home')
    project=Project.objects.get(id=id)
    if request.method=='POST':
        form=ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('prolist')
    else:
        form=ProjectForm(instance=project)
    return render(request,'project_create.html',{'form':form,'save':'save'})

@login_required
def project_delete(request,id):
    if not request.user.is_staff:
        return redirect('home')
    project=Project.objects.get(id=id)
    project.delete()
    return redirect('prolist')

@login_required
def logoutfun(request):
    if not request.user.is_staff:
        return redirect('home')
    logout(request)
    return redirect('home')

@login_required
def project_list_admin(request):
    if not request.user.is_staff:
        return redirect('home')
    project=Project.objects.all()
    return render(request,'project_list.html',{'projects':project})

@login_required
def task_list_admin(request):
    if not request.user.is_staff:
        return redirect('home')
    task=Task.objects.all()
    return render(request,'task_list.html',{'task':task})

@login_required
def task_create_page(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.POST:
        task=TaskForm(request.POST)
        if task.is_valid():
            task.save()
            return redirect('taskpage')
    else:
        task=TaskForm()
    return render(request,'task_create.html',{'task':task,'save':'create'})

@login_required
def edit_task(request,id):
    if not request.user.is_staff:
        return redirect('home')
    tsk=Task.objects.get(id=id)
    if request.method=='POST':
        task=TaskForm(request.POST,instance=tsk)
        if task.is_valid():
            task.save()
            return redirect('taskpage')
    else:
        task=TaskForm(instance=tsk)
    return render(request,'task_create.html',{'task':task,'save':'save'})

@login_required
def task_delete(request,id):
    if not request.user.is_staff:
        return redirect('home')
    task=Task.objects.get(id=id)
    task.delete()
    return redirect('taskpage')

@login_required
def user_task_details(request):
    tsk=Task.objects.filter(assigned_to=request.user)
    status=request.GET.get("status")
    priority=request.GET.get('priority')
    search=request.GET.get('search')
    if status:
        tsk=tsk.filter(status=status)
    if priority:
        tsk=tsk.filter(priority=priority)
    if search:
        tsk = tsk.filter(Q(title__icontains=search) | Q(project__name__icontains=search))
    return render(request,'user_task_details.html',{'tsk':tsk})

@login_required
def user_task_update(request,id,status):
    task=get_object_or_404(Task,id=id,assigned_to=request.user)
    task.status=status
    task.save()
    return redirect('user_task_details')

def employee_create(request):
    form=EmployeeForm()
    if request.POST:
        form=EmployeeForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['email']
            emp_id=generate_emp_id()
            password=generate_password()
            user=User.objects.create_user(username=username,email=username,password=password)
            emp=form.save(commit=False)
            emp.emp_id=emp_id
            emp.user=user
            emp.save()
            send_employee_credentials(username, password)
            return redirect('admin_home')
    return render(request,'admin_employee_create.html',{'form':form})

def employee_list(request):
    emp=Employee.objects.all()
    return render(request,'admin_employee_list.html',{'emp':emp})

def edit_employee(request,id):
    employee=Employee.objects.get(id=id)
    if request.POST:
        form=EmployeeForm(request.POST,instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form=EmployeeForm(instance=employee)
    return render(request,'admin_employee_create.html',{'form':form})

def employee_delete(request,id):
    emp=Employee.objects.get(id=id)
    emp.delete()
    return redirect('admin_employee_list.html')

def send_employee_credentials(email, password):
    subject = 'Your Login Credentials'
    message = f"""
Dear User,

Your account has been created successfully.

Username: {email}
Password: {password}

Please log in and change your password after first login.

Regards,
Admin Team
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,   # Admin email
        [email],                    # Employee email
        fail_silently=False,
    )

@login_required
def force_change_credentials(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('force_change_credentials')
        user = request.user
        user.username = new_username
        user.set_password(new_password)
        user.save()
        user.employee.is_first_login = False
        user.employee.save()
        logout(request)
        messages.success(request,'Username and password changed successfully. Please login again.')
        return redirect('home')
    return render(request, 'force_password_change.html')

def user_profile(request):
    employee=Employee.objects.get(user=request.user)
    if request.POST:
        form=User_Update(request.POST,instance=employee)
        if form.is_valid():
            form.save()
            return redirect('userpage')
    else:
        form=User_Update(instance=employee)
    return render(request,'user_profile.html',{'user':form})

def block_employee(request,id):
    print('aaa')
    user=get_object_or_404(User,id=id)
    user.is_active=False
    user.save()
    return redirect('employee_list')

def unblock_employee(request,id):
    user=get_object_or_404(User,id=id)
    user.is_active=True
    user.save()
    return redirect('employee_list')



