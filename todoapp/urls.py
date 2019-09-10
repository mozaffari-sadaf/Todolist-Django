from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'todoapp'
urlpatterns = [
	path('', views.index, name='index'),
	path('generalTasks/', views.generalTasks, name='generalTasks'),
	path('generalTasks/editList/', views.editList, name='editList'),
	path('generalTasks/removeList/', views.removeList, name='removeList'),
	path('<int:list_id>/', views.todoItem, name='items'),
	path('editItem/', views.editItem, name='editItem'),
	path('removeItem/', views.removeItem, name='removeItem'),
	path('toggleCheck/', views.toggleCheck, name='toggleCheck'),
	path('taskToggleCheck/', views.taskToggleCheck, name='taskToggleCheck'),
	path('isChecked/', views.isChecked, name='isChecked'),
	path('taskIsChecked/', views.taskIsChecked, name='taskIsChecked'),
	path('getMaxDate/', views.getMaxDate, name='getMaxDate'),
	path('generalTasks/taskDone/', views.taskDone, name='taskDone'),
	path('getTaskTitle/', views.getTaskTitle, name='getTaskTitle'),
	path('signup/', views.signup, name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name='todoapp/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='todoapp/logout.html'), name='logout'),
]