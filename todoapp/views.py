from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import ToDoList, ToDoItem


#To display list of todolists
def index(request):
	
	todolist = ToDoList.objects.all()
	
	if request.method == "POST":
		
		if "save" in request.POST:
			title = request.POST["title"]
			deadline = str(request.POST["deadline"])
			ToDo = ToDoList(title=title,deadline=deadline)
			ToDo.save()
			return redirect("/todoapp")
		
	return render(request, "todoapp/index.html", {"todolist": todolist})
			

#To remove a todolist from database
def removeList(request):
	
	list_id = request.GET.get('listid', None)
	
	removed_list = ToDoList.objects.get(pk=list_id)
	removed_list.delete()
	
	data = {'is_removed': True}
	
	return JsonResponse(data)
	

# To edit date or title of a todolist
def editList(request):

	new_title = request.GET.get("titleValue",None)
	new_date = request.GET.get("dateValue", None)
	list_id = request.GET.get("listId", None)
		
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
			time_to_do = str(request.POST["due_date"]) + "T" + str(request.POST["due_time"])+"Z"
			item = ToDoItem(todolist_id=list_id,title=to_do_name,time_to_do=time_to_do)
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
def removeItem(request, list_id=None):
	
	todo_id = request.GET.get('todoid', None)
	
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
def toggleCheck(request, list_id=None):
	
	todo_id = request.GET.get('todoid', None)
	
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
def isChecked(request, list_id=None):
	todo_id = request.GET.get('todoid', None)
	
	checked_item = ToDoItem.objects.get(pk=todo_id)
	
	if checked_item.done == True:
		data = {'is_checked': True}
	else:
		data = {'is_checked': False}
	
	return JsonResponse(data)
	

#To change the title or date of a todoitem
def editItem(request, list_id=None):

	new_title = request.GET.get("titleValue",None)
	new_date = request.GET.get("dateValue", None)
	new_time = request.GET.get("timeValue", None)
	item_id = request.GET.get("itemId", None)
		
	edited_item = ToDoItem.objects.get(pk=item_id)
	edited_item.title = new_title
	
	if new_date != "" or new_time != "":
		edited_item.time_to_do = new_date + " " + new_time
	
	ret_data = {'new_date': edited_item.time_to_do}
	
	edited_item.save();
		
	return JsonResponse(ret_data);