from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    #username = models.TextField(default='noname')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.TextField()
    end = models.TextField()
    stops = models.TextField(null=True, blank=True)
    stops_arr = models.TextField(default='', null=True, blank=True)
    date = models.DateField()
    time_dep = models.FloatField()
    time_arr = models.FloatField()
    car_model = models.TextField()
    car_cap = models.IntegerField()
    cigs = models.BooleanField()
    pets = models.BooleanField()
    price = models.FloatField()

  

class Driver_hist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.TextField()
    end = models.TextField()
    stops = models.TextField()
    stops_arr = models.TextField(default='')
    date = models.DateField()
    time_dep = models.FloatField()
    time_arr = models.FloatField()
    car_model = models.TextField()
    car_cap = models.IntegerField()
    cigs = models.BooleanField()
    pets = models.BooleanField()
    price = models.FloatField()

class Passenger(models.Model):
    id = models.AutoField(primary_key=True)
    #username = models.TextField(default='noname')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.TextField()
    end = models.TextField()
    distance = models.FloatField()
    date = models.DateField()
    time_dep = models.FloatField()
    time_arr = models.FloatField()
    cigs = models.BooleanField()
    pets = models.BooleanField()
    max_cost = models.FloatField()

    

class Passenger_hist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.TextField()
    end = models.TextField()
    distance = models.FloatField()
    date = models.DateField()
    time_dep = models.FloatField()
    time_arr = models.FloatField()
    cigs = models.BooleanField()
    pets = models.BooleanField()
    max_cost = models.FloatField()
    
class Ride(models.Model):
    ride_id = models.AutoField(primary_key=True)
    driver_ride_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    passenger_ride_id = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    driver_username = models.TextField(default='noname')
    passenger_username = models.TextField(default='noname')
    #driver_user = models.ForeignKey(User, on_delete=models.CASCADE)
    #passenger_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    pick_up = models.TextField()
    drop_off = models.TextField()
    car_model = models.TextField(default="car")

class Ride_hist(models.Model):
    ride_id = models.AutoField(primary_key=True)
    driver_username = models.TextField(default='noname')
    passenger_username = models.TextField(default='noname')
    date = models.DateField()
    pick_up = models.TextField()
    drop_off = models.TextField()
    car_model = models.TextField(default="car")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.TextField()
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField(blank = True, null=True)
    driver_ride_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    message = models.TextField()

    