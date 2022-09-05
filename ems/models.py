from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Department(models.Model):
    name=models.CharField(max_length=70, unique=True)
    description=models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.name
    
class Role(models.Model):
    name=models.CharField(max_length=70, unique=True)
    description=models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.name

class Address(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, blank=True,null=True)
    address=models.CharField(max_length=150)
    street=models.CharField(max_length=70)
    locality=models.CharField(max_length=70)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pincode=models.FloatField(max_length=50)
    country=models.CharField(max_length=50, default='India')
    def __str__(self):
        return self.city



class Employee(models.Model):
    empid=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    father_name=models.CharField(max_length=50)
    avtar=models.ImageField(upload_to='employee_profile_images', blank=True , default='profile.jpg')
    dob=models.DateField()
    email=models.EmailField(max_length=100)
    mobile_no=models.IntegerField()
    emergency_mobile_no=models.IntegerField(null=True,blank=True)
    address=models.OneToOneField(Address, on_delete=models.CASCADE,blank=True, null=True,)
    designation=models.CharField(max_length=70)
    role=models.ForeignKey(Role, on_delete=models.SET_NULL,blank=True, null=True,)
    department=models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True,)
    joining_date=models.DateField()
    status=models.CharField(max_length=15)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url=self.avtar.url
        except:
            url=''
        return url

class Attendance(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    intime=models.TimeField(blank=True, null=True)
    outtime=models.TimeField(blank=True,null=True)
    present=models.BooleanField(default=False)
    date=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.employee.name
    
class Leave(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    date_from=models.DateField()
    date_to=models.DateField()
    description=models.CharField(max_length=150)
    type=models.CharField(max_length=70)
    reply=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.employee.name

class Events(models.Model):
    title=models.CharField(max_length=150)
    description=models.TextField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    date=models.DateField()
    is_completed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


