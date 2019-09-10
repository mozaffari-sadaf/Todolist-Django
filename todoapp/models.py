from django.db import models
from django.contrib.auth.models import User


class ToDoList(models.Model):
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	deadline = models.DateField()
	done = models.BooleanField(default=False)	 #If the "done" field of all its items = done --> True
	hasItem = models.BooleanField(default=False) #If a task doesn't have any items, it should be considered in the user's calendar itself.
	
	def __str__(self):
		return self.title
		
#Each list could have some to-do-items.		
class ToDoItem(models.Model):
	
	todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	date_to_do = models.DateField(null=True, blank=True)
	time_to_do = models.TimeField(null=True, blank=True)
	done = models.BooleanField(default=False)
	important = models.BooleanField(default=False)
	
	def __str__(self):
		return self.title
		