from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
import vobject
import smtplib
from .forms import EmployeeForm, EventForm
from .models import Employee, Events
# Create your views here.

def employee_List(request,id=0):
    context = {'employee_list' : Employee.objects.all(), 'page_name': 'Users Management'}
    return render(request, "employee_register/employee_list.html", context)
        
def employee_form(request,id=0):
    
    if request.method == "GET":
        if id==0:
            form = EmployeeForm()
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(instance=employee)
        return render(request, "employee_register/employee_form.html", {'form': form,'page_name' : 'Users Register' })
    else:
        if id==0:
            form = EmployeeForm(request.POST)
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/list')
        else:
            return redirect('/')
            
def employee_delete(request,id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect('/list')

def ics_create(request):
    if request.method == "GET":
        form = EventForm()
    else:
        form = EventForm(request.POST)
    if form.is_valid():
        form.save()
        context = {'employee_list' : Employee.objects.all(), 'send': True,'page_name': 'Users Management'}
        return render(request, "employee_register/employee_list.html", context)
    return render(request, "employee_register/ics_create.html", {'form': form, 'page_name': 'Event Edite'})

def ics_send(request):

    user_id = request.POST.getlist('selected[]')
    reciver = []
    for uid in user_id:
        email_address = Employee.objects.get(pk=uid)
        reciver.append(email_address.email)

    event = Events.objects.all().order_by('-id')[0]

    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
    vevent = cal.add('vevent')
    vevent.add('dtstart').value = event.start_time
    vevent.add('dtend').value = event.end_time
    vevent.add('summary').value = event.summary
    vevent.add('description').value = event.description
    icalstream = cal.serialize()

    print(icalstream)

    part = MIMEText(icalstream,'calendar')
    part.add_header('Filename','Event.ics') 
    part.add_header('Content-Disposition','attachment; filename=Event.ics')

    subject = settings.EMEIL_TITLE, ''' '''
    from_email = settings.EMAIL_HOST_USER,

    to = ", ".join(reciver)
    sender_email = from_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD) 
        server.sendmail(sender_mail, to, part.as_string())
        server.quit()
        print('------------>Success')
        result = True
    except:
        print('------------->Error')
        result = False
        
    return JsonResponse(result, safe=False)
