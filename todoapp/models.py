from django.db import models


class ToDoList(models.Model):
	
	title = models.CharField(max_length=300)
	deadline = models.DateField()
	done = models.BooleanField(default=False)	#If the "done" field of all its items = done --> True
	
	def __str__(self):
		return self.title
		
#Each list could have some to-do-items.		
class ToDoItem(models.Model):
	
	todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	time_to_do = models.DateTimeField()
	done = models.BooleanField(default=False)
	
	def __str__(self):
		return self.title
		
		

	