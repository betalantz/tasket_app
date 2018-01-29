from django.shortcuts import render, redirect
from ..user_app.models import *
from models import *
from django.contrib import messages
from ..user_app.views import sessionCheck
import datetime
# from django.core.urlresolvers import reverse

def test(request):
    print '>'*20, 'welcome to appoint_app views'

def dashboard(request):
    if sessionCheck(request)==False:
        return redirect ('/')
    
    context = {
        'today' : datetime.date.today(),
        'curr_apts' : Appointment.objects.filter(user=request.session['user_id']).filter(date=datetime.date.today()),
        'later_appoints' : Appointment.objects.filter(user=request.session['user_id']).filter(date__gt=datetime.date.today())
        }
    # print context['user'].heroLikes.all()
    return render(request, 'appoint_app/dashboard.html', context)

def addTask(request):
    results = Appointment.objects.appointValidator(request, request.POST)
    if results['status']==False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/appoint')
    messages.success(request, 'Your task has been added.')
    return redirect('/appoint')

def edit(request, task_id):
    if sessionCheck(request) == False:
        return redirect('/appoint')

    context = {
        'task': Appointment.objects.get(id = task_id),
    }
    return render(request, 'appoint_app/edit.html', context)

def update(request, task_id):
    update = Appointment.objects.get(id = task_id)
    if request.POST['task']:
        update.task = request.POST['task']
    if request.POST['status']:
        update.status = request.POST['status']
    if request.POST['apt_date']:
        update.date = request.POST['apt_date']
    if request.POST['apt_time']:
        update.time = request.POST['apt_time']
    update.save()
    return redirect ('/appoint')

def delete(request, task_id):
    thisTask = Appointment.objects.get(id = task_id)
    thisTask.delete()
    return redirect ('/appoint')
