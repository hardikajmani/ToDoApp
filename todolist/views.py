from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import TodoList, Category, Priority

from todolist.forms import SignUpForm, ExportForm


@login_required(login_url='/accounts/login/')
# Create your views here.

def index(request): #the index view
    todos      = TodoList.objects.all()
    categories = Category.objects.all() #getting all categories with object manager
    priorities = Priority.objects.all() #getting all priorites with object manager
    status     = "Incomplete"
    message = ""        

    if request.method == "POST": #checking if the request method is a POST
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date
            category = request.POST["category_select"] #category
            priority = request.POST["priority_select"] #category
            content = title + " -- " + date + " " + category + " priority@" + priority + " " + "Status: \"" #content
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category), priority=Priority.objects.get(name = priority), status = status)
            Todo.save() #saving the todo 
            return redirect("/",{"message":message}) #reloading the page

        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            if checkedlist == []:
                message = "Please Choose atleast one task!"
            else:    
                for todo_id in checkedlist:
                    todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
                    todo.delete() #deleting todo
                message  = "Updated!"
            return redirect("/",{"message":message})

        if "taskComplete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            if checkedlist == []:
                message = "Please Choose atleast one task!"
            else:
                for todo_id in checkedlist:
                    todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
                    todo.status = "Complete" #finshing todo
                    todo.save()
                message  = "Updated!"
            return redirect("/",{"message":message})
            

        if "deleteAll" in request.POST: #checking if there is a request to delete a todo
            for todo in todos:
                todo.delete()

    return render(request, "index.html", {"todos": todos, "categories":categories, "priorities":priorities, "status":status, "message":message})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def export(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            todos = TodoList.objects.all()
            for todo in todos:
                task = todo.content + todo.status + "\""
                message += ("<br>" + task)

            send_mail('Exported ToDO Tasks', message, 'no_reply@todoapp.com', [email], html_message=message )
            flag = True
            return redirect('/')
    else:
        form = ExportForm()
    return render(request, 'export.html', {'form': form})

