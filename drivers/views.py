from django.contrib.auth import login, authenticate
from .forms import SignUpForm, DriverForm, PassengerForm, EditProfileForm, MessageForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ride, Driver, Passenger, Profile, Message
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from .google_maps import get_distance, get_arrivals
import time
import datetime
from calendar import timegm
from .help_funcs import time_to_epoch

# Create your views here.


def home_view(request, *args, **kwargs):
        
    info = {}
    if request.user.is_authenticated:
        info['first_name'] = request.user.first_name
    
    return render(request, 'home.html', info)

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def profile_view(request):
    if request.user.is_authenticated:
        driver_rides = Ride.objects.filter(driver_username = request.user.username)
        passenger_rides = Ride.objects.filter(passenger_username = request.user.username)
        offered_driver_rides = Driver.objects.filter(username = request.user.username)
        offered_passenger_rides = Passenger.objects.filter(username = request.user.username)

        if len(driver_rides) == 0:
            driver_flag = False
        else:
            driver_flag = True

        if len(passenger_rides) == 0:
            passenger_flag = False
           
        else:
            passenger_flag = True

        if len(offered_driver_rides) == 0:
            offered_driver_flag = False
        else:
            offered_driver_flag = True

        if len(offered_passenger_rides) == 0:
            offered_passenger_flag = False
        else:
            offered_passenger_flag = True
           
        
        #d_dates = driver_rides.date


        info = {
            'passenger_flag':passenger_flag,
            'driver_flag':driver_flag,
            'offered_passenger_flag':offered_passenger_flag,
            'offered_driver_flag':offered_driver_flag,
            'driver_rides':driver_rides,
            'passenger_rides':passenger_rides,
            'offered_driver_rides':offered_driver_rides,
            'offered_passenger_rides':offered_passenger_rides,
        }
        return render(request, 'profile.html', info)
    else:
        return redirect('home')

def add_driver_view(request):
    form = DriverForm(request.POST)
    
    if form.is_valid() and request.user.is_authenticated:

        time_string = str(form.cleaned_data['date']) + 'T' + str(form.cleaned_data['time_dep'])
        time_stripped = time.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
        epoch_time_dep = timegm(time_stripped)
        args = [form.cleaned_data['start'],]
        for el in form.cleaned_data['stops'].split():
            args.append(el)
        args.append(form.cleaned_data['end'])
        arr_times = get_arrivals(args)

        for i in range(len(arr_times)):
            arr_times[i] = epoch_time_dep + arr_times[i]

        arr_times_str = ''
        for el in arr_times[:-1]:
            arr_times_str = arr_times_str + str(el) + ' '

        driver = Driver()
        driver.username = request.user.username
        driver.start = form.cleaned_data['start']
        driver.end = form.cleaned_data['end']
        driver.stops = form.cleaned_data['stops']
        driver.stops_arr = arr_times_str
        driver.date = form.cleaned_data['date']
        driver.time_dep = epoch_time_dep
        driver.time_arr = arr_times[-1]
        driver.car_model = form.cleaned_data['car_model']
        driver.car_cap = form.cleaned_data['car_cap']
        driver.cigs = form.cleaned_data['cigs']
        driver.pets = form.cleaned_data['pets']
        driver.price = form.cleaned_data['price']
        driver.save()
        return redirect('profil')
    else:
        form = DriverForm()
    return render(request, 'add_driver.html', {'form':form})

def add_passenger_view(request):
    form = PassengerForm(request.POST)
    if form.is_valid() and request.user.is_authenticated:

        distance = get_distance((form.cleaned_data['start'],form.cleaned_data['end']))
        time_string = str(form.cleaned_data['date']) + 'T' + str(form.cleaned_data['time_dep'])
        print(time_string)
        time_stripped = time.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
        epoch_time_dep = timegm(time_stripped)
        print(epoch_time_dep)

        passenger = Passenger()
        passenger.username = request.user.username
        passenger.start = form.cleaned_data['start']
        passenger.end = form.cleaned_data['end']
        passenger.distance = distance[0]/1000
        passenger.date = form.cleaned_data['date']
        passenger.time_dep = epoch_time_dep
        passenger.time_arr = epoch_time_dep+distance[1]
        passenger.cigs = form.cleaned_data['cigs']
        passenger.pets = form.cleaned_data['pets']
        passenger.max_cost = form.cleaned_data['max_cost']
        passenger.save()
        return redirect('profil')
    elif request.user.is_authenticated:
        form = PassengerForm()
    else:
        return redirect('profil')
    return render(request, 'add_passenger.html', {'form':form})

def edit_driver_ride_view(request, id=None):

    ride = get_object_or_404(Driver, id=id)
    if ride.username != request.user.username:
        return HttpResponseForbidden()
    
    t = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(ride.time_dep))
    data = {
        'start':ride.start,
        'end':ride.end,
        'stops':ride.stops,
        'date':t[:10],
        'time_dep':t[11:16],
        'car_model':ride.car_model,
        'car_cap':ride.car_cap,
        'cigs':ride.cigs,
        'pets':ride.pets, 
        'price':ride.price
        }
    form = DriverForm(request.POST)
    if request.POST and form.is_valid():
        print('inside if')

        time_string = str(form.cleaned_data['date']) + 'T' + str(form.cleaned_data['time_dep'])
        time_stripped = time.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
        epoch_time_dep = timegm(time_stripped)
        args = [form.cleaned_data['start'],]
        for el in form.cleaned_data['stops'].split():
            args.append(el)
        args.append(form.cleaned_data['end'])
        arr_times = get_arrivals(args)

        for i in range(len(arr_times)):
            arr_times[i] = epoch_time_dep + arr_times[i]

        arr_times_str = ''
        for el in arr_times[:-1]:
            arr_times_str = arr_times_str + str(el) + ' '

        ride.start = form.cleaned_data['start']
        ride.end = form.cleaned_data['end']
        ride.stops = form.cleaned_data['stops']
        ride.stops_arr = arr_times_str
        ride.date = form.cleaned_data['date']
        ride.time_dep = epoch_time_dep
        ride.time_arr = arr_times[-1]
        ride.car_model = form.cleaned_data['car_model']
        ride.car_cap = form.cleaned_data['car_cap']
        ride.cigs = form.cleaned_data['cigs']
        ride.pets = form.cleaned_data['pets']
        ride.price = form.cleaned_data['price']
        ride.save()
        
        return redirect('profil')
    elif not form.is_valid():
        form = DriverForm(initial = data)
        print('invalid form')
    else:
        form = DriverForm(initial = data)
    
    return render(request, 'edit_driver.html', {'form':form})

def edit_passenger_ride_view(request, id=None):

    ride = get_object_or_404(Passenger, id=id)
    if ride.username != request.user.username:
        return HttpResponseForbidden()
    
    t = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(ride.time_dep))
    data = {
        'start':ride.start,
        'end':ride.end,
        'date':t[:10],
        'time_dep':t[11:16],
        'cigs':ride.cigs,
        'pets':ride.pets, 
        'max_cost':ride.max_cost
        }

    form = PassengerForm(request.POST)
    if form.is_valid() and request.POST:

        distance = get_distance((form.cleaned_data['start'],form.cleaned_data['end']))
        time_string = str(form.cleaned_data['date']) + 'T' + str(form.cleaned_data['time_dep'])
        print(time_string)
        time_stripped = time.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
        epoch_time_dep = timegm(time_stripped)
        print(epoch_time_dep)

        ride.start = form.cleaned_data['start']
        ride.end = form.cleaned_data['end']
        ride.distance = distance[0]/1000
        ride.date = form.cleaned_data['date']
        ride.time_dep = epoch_time_dep
        ride.time_arr = epoch_time_dep+distance[1]
        ride.cigs = form.cleaned_data['cigs']
        ride.pets = form.cleaned_data['pets']
        ride.max_cost = form.cleaned_data['max_cost']
        ride.save()
        return redirect('profil')
    elif not form.is_valid():
        form = PassengerForm(initial = data)
    else:
        form = PassengerForm(initial = data)
    return render(request, 'edit_passenger.html', {'form':form})

def edit_profile_view(request):
    user = get_object_or_404(User, username=request.user.username)
    rides_d = Ride.objects.filter(driver_username=request.user.username)
    rides_p = Ride.objects.filter(passenger_username=request.user.username)
    passenger = Passenger.objects.filter(username=request.user.username)
    print(len(passenger))
    driver = Driver.objects.filter(username=request.user.username)
        
    form = EditProfileForm(request.user.username, request.POST, instance=request.user)
    if request.POST and form.is_valid():
        for el in rides_d:
            el.driver_username = form.cleaned_data['username']
            el.save()

        for el in rides_p:
            el.passenger_username = form.cleaned_data['username']
            el.save()

        for el in passenger:
            el.username = form.cleaned_data['username']
            print('TU')
            el.save()

        for el in driver:
            el.username = form.cleaned_data['username']
            el.save()
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.profile.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        
        return redirect('home')
    elif not form.is_valid():
        print(form.errors)
        form = EditProfileForm(request.user.username, instance=request.user)
        
    else:
        form = EditProfileForm(request.user.username, instance=request.user)
    return render(request, 'edit_profile.html', {'form':form})

def delete_passenger_view(request, id = None):
    if request.user.is_authenticated:
        passenger = get_object_or_404(Passenger, id=id)
        info = {'ride':passenger, 'who':'pasażer'}
        passenger.delete()
        return render(request, 'delete.html', info)
    else:
        redirect('home')

def delete_driver_view(request, id = None):
    if request.user.is_authenticated:
        driver = get_object_or_404(Driver, id=id)
        info = {'ride':driver, 'who':'kierowca'}
        driver.delete()
        return render(request, 'delete.html', info)
    else:
        redirect('home')

def delete_p_ride_view(request, id = None):
    if request.user.is_authenticated:
        ride = get_object_or_404(Ride, ride_id=id)
        info = {'ride':ride, 'who':'pasażer'}
        ride.delete()
        return render(request, 'delete.html', info)
    else:
        redirect('home')

def delete_d_ride_view(request, id = None):
    if request.user.is_authenticated:
        ride = get_object_or_404(Ride, ride_id=id)
        info = {'ride':ride, 'who':'kierowca'}
        ride.delete()
        return render(request, 'delete.html', info)
    else:
        redirect('home')

def ride_chat_view(request, id = None):
    form = MessageForm(request.POST)
    messages = Message.objects.filter(driver_ride_id=id)
    msgs = []
    drvr = get_object_or_404(Driver, id=id)
    for i in range(len(messages)):
        msg = []
        msg.append(messages[i].user)                        # 0 - user
        if messages[i].user == drvr.username:
            msg.append(True)                                # 1 - if driver
        else:
            msg.append(False)
        date = str(messages[i].date_created)                # 2 - date
        msg.append(date[:16])
        msg.append(messages[i].message)                     # 3 - message
        msgs.append(msg)
    info = {}
    info['messages'] = msgs
    if request.user.is_authenticated and request.POST and form.is_valid():
        #print('tuuuuuuuu')
        msg = Message()
        msg.date_created = datetime.datetime.now()
        msg.driver_ride_id = get_object_or_404(Driver, id=id)
        msg.user = request.user.username
        msg.message = form.cleaned_data['message']
        msg.save()
        path = '/drivers/ride_chat/'+str(id)
        return redirect(path)
    elif request.user.is_authenticated:
        #print('xdddddddd')
        form = MessageForm()
        info['form'] = form
       # return redirect(path)
    else:
        redirect('home')
    return render(request, 'chat.html', info)