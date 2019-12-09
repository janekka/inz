from django.contrib import admin

# Register your models here.
from .models import Driver, Passenger, Ride, Profile

admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Ride)
admin.site.register(Profile)
