from django.db import models
from django.conf import settings
# Create your models here.

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=20,blank=False)
    lastname = models.CharField(max_length=20,blank=False)
    email = models.EmailField(unique=True,blank=False)
    phone = models.CharField(max_length=10,null=True)
    address = models.TextField()
    place=models.CharField(max_length=30, blank=True)
    availability = models.IntegerField(default=0)
    district = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    password = models.CharField(max_length=256)
    usertype = models.CharField(max_length=20)

class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50)
    skill_description = models.TextField()

class House_Maid(models.Model):
    maid_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    experience = models.IntegerField()
    availability = models.IntegerField(default=0)
    firstname = models.CharField(max_length=20, blank=False)
    lastname = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, blank=False)
    place=models.CharField(max_length=30, blank=True)
    district = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=10, null=True)
    profilepic = models.ImageField(upload_to='maid_pic', null=True, blank=True)
    address = models.TextField()

class Home_Nurse(models.Model):
    nurse_id = models.AutoField(primary_key=True)
    usertype = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    experience = models.IntegerField()
    availability = models.IntegerField(default=0)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    place=models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    district = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=15)
    profilepic = models.ImageField(upload_to='nurse_pic', null=True, blank=True)
    address = models.TextField()

class Carpenter(models.Model):
    carpenter_id = models.AutoField(primary_key=True)
    usertype = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    experience = models.IntegerField()
    availability = models.IntegerField(default=0)
    district = models.CharField(max_length=20, blank=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    place=models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    profilepic = models.ImageField(upload_to='carpenter_pic', null=True, blank=True)
    address = models.TextField()

class Electrician(models.Model):
    electrician_id = models.AutoField(primary_key=True)
    usertype = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    experience = models.IntegerField()
    availability = models.IntegerField(default=0)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    district = models.CharField(max_length=20, blank=True)
    place=models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    profilepic = models.ImageField(upload_to='electrician_pics', null=True, blank=True)
    address = models.TextField()

class Plumber(models.Model):
    plumber_id = models.AutoField(primary_key=True)
    usertype = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    experience = models.IntegerField()
    availability = models.IntegerField(default=0)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    place=models.CharField(max_length=30, blank=True)
    district = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    profilepic = models.ImageField(upload_to='plumber_pics', null=True, blank=True)
    address = models.TextField()


class Booking(models.Model):
    # Foreign key to the Users table for the worker
    worker_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='bookings')
    
    # Field to identify the type of worker
    worker_type = models.CharField(max_length=50, choices=[
        ('House Maid', 'House Maid'),
        ('Carpenter', 'Carpenter'),
        ('Plumber', 'Plumber'),
        ('Electrician', 'Electrician'),
        ('Home Nurse', 'Home Nurse'),
    ])
    
    # Foreign key to the Users table for the customer
    customer_id= models.ForeignKey('Users', on_delete=models.CASCADE, related_name='customer_bookings')
    
    # Date and time of the appointment
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    
    # Address where the service will be provided
    address = models.TextField()
    
    # Status of the booking
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')