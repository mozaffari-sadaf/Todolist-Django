from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'todoapp'
urlpatterns = [
	path('', views.index, name='index'),
	path('general_tasks/', views.general_tasks, name='general-tasks'),
	path('general_tasks/edit_list/', views.edit_list, name='edit-list'),
	path('general_tasks/remove_list/', views.remove_list, name='remove-list'),
	path('<int:list_id>/', views.todo_item, name='items'),
	path('edit_item/', views.edit_item, name='edit-item'),
	path('remove_item/', views.remove_item, name='remove-item'),
	path('item_toggle_check/', views.item_toggle_check, name='item-toggle-check'),
	path('task_toggle_check/', views.task_toggle_check, name='task-toggle-check'),
	path('item_is_checked/', views.item_is_checked, name='item-is-checked'),
	path('task_is_checked/', views.task_is_checked, name='task-is-checked'),
	path('get_max_date/', views.get_max_date, name='get-max-date'),
	path('general_tasks/task_done/', views.task_done, name='task-done'),
	path('get_task_title/', views.get_task_title, name='get-task-title'),
	path('signup/', views.signup, name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name='todoapp/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='todoapp/logout.html'), name='logout'),
]