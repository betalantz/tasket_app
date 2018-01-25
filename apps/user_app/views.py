from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages

# def test(request):
#     print "/\/\/\/\/\/ Create your views here."

def index(request):
    return render(request, "user_app/index.html") 

def register(request):
    results = User.objects.register_validator(request.POST)
    if results['status']==False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/index')
    user = User.objects.createUser(request.POST)
    messages.success(request, 'You registered successfully! Please log in.')
    return redirect('/')

def login(request):
    results = User.objects.login_validator(request.POST)
    if results['status']==False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/index')
    # store a user auth token in sessions to allow a session check
    request.session['user_id']=results['user'].id
    request.session['user_name']=results['user'].name

    storage = messages.get_messages(request)
    storage.used = True
    return redirect('/appoint')
    # return HttpResponse("Login success")

def sessionCheck(request):
    try:
        return request.session['user_id']
    except:
        return False

def logout(request):
    request.session.flush() #also check .clear() method. What are advantges?
    return redirect ('/')
