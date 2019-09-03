from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models.functions import Extract, ExtractWeek
from .models import ToDoList, ToDoItem
import datetime


#To display items of each day, week, or month
def index(request):

	today = timezone.now().date()
	current_week = today.strftime("%V")
	current_month = today.month
	
	daily_list = ToDoItem.objects.filter(date_to_do=str(today)).order_by('done','time_to_do','-important');
	
	weekly_list = ToDoItem.objects.filter(date_to_do__week=current_week).order_by('done','date_to_do','-important','time_to_do'); 
	
	monthly_list = ToDoItem.objects.filter(date_to_do__month=current_month).order_by('done','date_to_do','-important','time_to_do');
	
	return render(request, "todoapp/index.html", {"daily_list": daily_list, "weekly_list": weekly_list, "monthly_list": monthly_list})
	

#To display list of general Tasks
def generalTasks(request):
	
	todolist = ToDoList.objects.all()
	
	if request.method == "POST":
		
		if "save" in request.POST:
			title = request.POST["title"]
			deadline = request.POST["deadline"]
			ToDo = ToDoList(title=title,deadline=deadline)
			ToDo.save()
			return redirect("/todoapp/generalTasks")
		
	return render(request, "todoapp/general.html", {"todolist": todolist})
			

#To remove a todolist from database
@csrf_exempt
def removeList(request):
	
	list_id = request.POST.get('listid', None)
	
	removed_list = ToDoList.objects.get(pk=list_id)
	removed_list.delete()
	
	data = {'is_removed': True}
	
	return JsonResponse(data)
	

# To edit date or title of a todolist
@csrf_exempt
def editList(request):

	new_title = request.POST.get("titleValue",None)
	new_date = request.POST.get("dateValue", None)
	list_id = request.POST.get("listId", None)
		
	edited_list = ToDoList.objects.get(pk=list_id)
	edited_list.title = new_title
	
	if new_date != "":
		edited_list.deadline = new_date
	
	ret_data = {'new_date': edited_list.deadline}
	
	edited_list.save();
		
	return JsonResponse(ret_data);

	
# To display items of a todolist and to show that if items have done or not
def todoItem(request, list_id):

	todolist = ToDoList.objects.get(id=list_id)
	
	todoitems = ToDoItem.objects.filter(todolist=list_id)
	step_number = todoitems.count() + 1
	
	context = {"todoitems": todoitems, "todolist":todolist, "step_number":step_number}
	
	if request.method == "POST":
		
		if "save" in request.POST:
			
			to_do_name = request.POST["title"]
			date_to_do = str(request.POST["due_date"])
			time_to_do = None
			
			if request.POST["due_time"] is not '':
				time_to_do = str(request.POST["due_time"])

			if request.POST["important"]:
				important = True
			else:
				important = False
				
			item = ToDoItem(todolist_id=list_id,title=to_do_name,date_to_do=date_to_do,time_to_do=time_to_do,important=important)
			item.save()
			
			items_count = ToDoItem.objects.filter(todolist_id=list_id).count()
			checked_items_count = ToDoItem.objects.filter(done=True, todolist_id=list_id).count()
	
			if items_count == checked_items_count:
				todolist.done = True;
			else:
				todolist.done = False;
		
			todolist.save();
			
			return HttpResponseRedirect("")
		
	return render(request, "todoapp/items.html", context)
	

#To remove an item and update both ToDoList and ToDoItem tables
@csrf_exempt
def removeItem(request, list_id=None):
	
	todo_id = request.POST.get('todoid', None)
	
	removed_item = ToDoItem.objects.get(pk=todo_id)
	todo_list_id = removed_item.todolist_id; 
	removed_item.delete()
	
	items_count = ToDoItem.objects.filter(todolist_id=todo_list_id).count()
	step_number = items_count + 1;
	
	checked_items_count = ToDoItem.objects.filter(done=True, todolist_id=todo_list_id).count()
	
	parent_list = ToDoList.objects.get(pk=removed_item.todolist_id)
	if items_count == checked_items_count:
		parent_list.done = True;
	else:
		parent_list.done = False;
		
	parent_list.save();
	
	data = {'is_removed': True, 'step_number':step_number}
	
	return JsonResponse(data)
	

#Toggle the "done" field of ToDoItem and change the "done" field of ToDoList if all the items have done or vice versa
@csrf_exempt
def toggleCheck(request, list_id=None):
	
	todo_id = request.POST.get('todoid', None)
	
	checked_item = ToDoItem.objects.get(pk=todo_id)
	
	if checked_item.done == False:
		checked_item.done = True
		data = {'is_checked': True}
	else:
		checked_item.done = False
		data = {'is_checked': False}
	
	checked_item.save()
	
	todo_list_id = checked_item.todolist_id;
	
	items_count = ToDoItem.objects.filter(todolist_id=todo_list_id).count()
	checked_items_count = ToDoItem.objects.filter(done=True, todolist_id=todo_list_id).count()
	
	parent_list = ToDoList.objects.get(pk=checked_item.todolist_id)
	if items_count == checked_items_count:
		parent_list.done = True;
	else:
		parent_list.done = False;
		
	parent_list.save();
		
	return JsonResponse(data)
	

#To check that if the "done" field of an item is set to True or False
def isChecked(request):
	todo_id = request.GET.get('todoid', None)
	
	checked_item = ToDoItem.objects.get(pk=todo_id)
	
	if checked_item.done == True:
		data = {'is_checked': True}
	else:
		data = {'is_checked': False}
	
	return JsonResponse(data)
	

#To change the title or date of a todoitem
@csrf_exempt
def editItem(request):
	
	new_time = None;
	if request.POST.get("timeValue", None) is not '':
		new_time = request.POST.get("timeValue", None)
	
	new_title = request.POST.get("titleValue",None)
	new_date = request.POST.get("dateValue", None)
	
	item_id = request.POST.get("itemId", None)
		
	edited_item = ToDoItem.objects.get(pk=item_id)
	edited_item.title = new_title
	
	# if new_date != "" and new_time != "":
	edited_item.date_to_do = new_date
	edited_item.time_to_do = new_time
	
	ret_data = {'new_date': edited_item.date_to_do,'new_time': edited_item.time_to_do}
	
	edited_item.save();
		
	return JsonResponse(ret_data);