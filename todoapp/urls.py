from django.urls import path

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
	path('isChecked/', views.isChecked, name='isChecked'),
]