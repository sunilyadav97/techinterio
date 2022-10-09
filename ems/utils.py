import random
import string

from .models import *
import datetime
from datetime import timedelta,timezone
from django.contrib.auth.models import User
from techinterio import settings
from django.core.mail import send_mail


def filterLeave():
    leaves=Leave.objects.filter(status='Pending')
    
    filterd_leaves=[]

    for leave in leaves:
        created_time=leave.created_at
        current_time=datetime.datetime.now(timezone.utc)
        difference=current_time-created_time
        if difference.days <= 2:
            filterd_leaves.append(leave)
        print('Filterd Leaves : ',filterd_leaves)
    return filterd_leaves



def generateId():
    id=''
    for i in range(0,6):
        id+=str(random.randint(0,9))
        
    if len(id) != 6:
        generateId()
    else:
        id=int(id)
        obj=DepartmentQuery.objects.filter(query_id=id).exists()
        if obj:
            generateId()
        else:
            return id
        
def expireConnect():
    try:
        connects=Connect.objects.all()
        for item in connects:
            create_time=item.created_at
            current_time=datetime.datetime.now(timezone.utc)
            difference=current_time-create_time

            compare_time=int(2)
            
            if difference.days >= compare_time:
                item.delete()
                print('Item Deleted')
            else:
                print('Time Need to complete')

    except Exception as e:
        print('Expire Connect Exception : ',e)
    
def checkIsLate(intime):
    split_intime=str(intime).split(":")
    intime_hour=int(split_intime[0])
    intime_minute=int(split_intime[1])
    if intime_hour == 9:
        if intime_minute >45:
            return True
    elif intime_hour >9:
        return True
    else:
        return False


def generateToken():
    token=''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))
    print(token)

    if len(token) !=20:
        generateToken()
    else:
        obj=Newuser.objects.filter(token=token).exists()
        
        if obj:
            generateToken()
        else:
            return token


def sendMail(username,domain):
    user=User.objects.get(username=username)
    print('send mail user :',user)
    email=user.email
    print('email ',email)
    newuser_obj=Newuser.objects.get(user=user)
    print('send mail new user :',newuser_obj)
    token=newuser_obj.token
    print(token)
    subject="Welcome To Techinterio"
    message="This is Verification Email by Admin \n \n \n Follow Link given below. \n You can add your personal Info by following link. \n \n Note- This link only work when you will be connected with Techinterio Internal Server. \n \n Link: http://"+domain+"/ems/verify/"+token
    # message="Hello Dear Clients"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list, fail_silently=True)
    print(message)
    return True

def AllocatedLeaveOperation():
    allocatedLeaves=AllocatedLeave.objects.all()
    for item in allocatedLeaves:
        employee=item.employee
        year=item.start_date.year

        all_attendance=Attendance.objects.filter(employee=employee)
        # print('Allocated Leaves Attedance : ',all_attendance)
        # print('Allocated Leaves Employee : ',employee)
        # print('Allocated Leaves Year : ',year)
        year_attendance=[]
        for i in all_attendance:
            if i.get_year() == year:
                year_attendance.append(i)
        is_late_count=0
        for i in year_attendance:
            if i.present == False:
                val=int(item.allocated)
                item.allocated=val-1
                item.save()
            if i.is_late == True:
                is_late_count+=1
        late=int(is_late_count/2)
        x=int(item.allocated)
        # item.allocated=x-late
        # item.save()

def reassignAllocatedLeave():
    allocatedLeaves=AllocatedLeave.objects.all()
    current_date=datetime.datetime.now().date()
    Year=current_date.year
    leapyear=False
    if Year % 400 == 0 or Year % 100 != 0 and  Year % 4 == 0:   
         leapyear=True
        
    for item in allocatedLeaves:
        start_date=item.start_date
        delta=current_date-start_date
        days=delta.days
        if not leapyear:
            if current_date.year > item.start_date.year or days >= 365:
                next_date=item.end_date+datetime.timedelta(days=1)
                end_date=next_date+datetime.timedelta(days=365)
                print('Next Date ',next_date)
                print('End Date ',end_date)
                item.start_date=next_date
                item.end_date=end_date
                item.allocated=18
                item.earn=0
                item.save()
        else:
            if current_date.year > item.start_date.year or days >= 366:
                next_date=item.end_date+datetime.timedelta(days=1)
                end_date=next_date+datetime.timedelta(days=366)
                print('Next Date ',next_date)
                print('End Date ',end_date)
                item.start_date=next_date
                item.end_date=end_date
                item.allocated=18
                item.earn=0
                item.save()

