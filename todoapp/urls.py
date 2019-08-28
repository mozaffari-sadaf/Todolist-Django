from django.urls import path

from . import views

app_name = 'todoapp'
urlpatterns = [
	path('', views.index, name='index'),
	path('editList/', views.editList, name='editList'),
	path('removeList/', views.removeList, name='removeList'),
	path('<int:list_id>/', views.todoItem, name='items'),
	path('<int:list_id>/editItem/', views.editItem, name='editItem'),
	path('<int:list_id>/removeItem/', views.removeItem, name='removeItem'),
	path('<int:list_id>/toggleCheck/', views.toggleCheck, name='toggleCheck'),
	path('<int:list_id>/isChecked/', views.isChecked, name='isChecked'),
]