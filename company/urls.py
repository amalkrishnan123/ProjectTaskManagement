from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('adminpage/',views.admin_home_page,name='admin_home'),
    path('userpage/',views.userpage,name='userpage'),
    path('logout',views.logoutfun,name='logout'),
    path('project creat/',views.project_create_page,name='projectpage'),
    path('editproject/<int:id>/',views.editproject,name='edit_project'),
    path('projectlist/',views.project_list_admin,name='prolist'),
    path('delete/<int:id>/',views.project_delete,name='project_delete'),
    path('task_list/',views.task_list_admin,name='taskpage'),
    path('task_create/',views.task_create_page,name='task_create'),
    path('edit_task/<int:id>/',views.edit_task,name='edit_task'),
    path('delete_task/<int:id>/',views.task_delete,name='delete_task'),
    path('user_task_details/',views.user_task_details,name='user_task_details'),
    path('user_task_updates/<int:id>/<str:status>/',views.user_task_update,name='user_task_update'),
    path('emp_creation/',views.employee_create,name='employee_creation'),
    path('emp_list/',views.employee_list,name='employee_list'),
    path('edit_employee/<int:id>/',views.edit_employee,name='edit_employee'),
    path('delete_employee/<int:id>/',views.employee_delete,name='delete_employee'),
    path('force-password-change/', views.force_change_credentials, name='force_change_credentials'),
    path('employee_profile',views.user_profile,name='emp_profile'),
    path('block_emp,<int:id>',views.block_employee,name='block'),
    path('unblock_emp,<int:id>',views.unblock_employee,name='unblock'),
]
