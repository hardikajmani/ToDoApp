from django.shortcuts import render, redirect
from .models import TodoList, Category, Priority



# Create your views here.
def index(request): #the index view
    todos      = TodoList.objects.all()
    categories = Category.objects.all() #getting all categories with object manager
    priorities  = Priority.objects.all() #getting all priorites with object manager
    status      = "Incomplete"
    if request.method == "POST": #checking if the request method is a POST
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date
            category = request.POST["category_select"] #category
            priority = request.POST["priority_select"] #category
            content = title + " -- " + date + " " + category + " priority@" + priority #content
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category), priority=Priority.objects.get(name = priority), status = status)
            Todo.save() #saving the todo 
            return redirect("/") #reloading the page
        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            for todo_id in checkedlist:
                todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
                todo.delete() #deleting todo

        if "taskComplete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            for todo_id in checkedlist:
                todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
                todo.status = "Complete" #finshing todo
                todo.save()

        if "deleteAll" in request.POST: #checking if there is a request to delete a todo
            for todo in todos:
                todo.delete()

    return render(request, "index.html", {"todos": todos, "categories":categories, "priorities":priorities, "status":status})
