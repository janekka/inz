from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class DriverForm(forms.Form):
    start = forms.CharField(label='start', max_length=20)
    end = forms.CharField(label='end', max_length=20)
    stops = forms.CharField(label='stops', max_length=100, required=False)
    date = forms.DateField(label='date', input_formats=['%d-%m-%Y', '%d/%m/%Y'])
    time_dep = forms.TimeField(label='time_dep')
    car_model = forms.CharField(label='car_model', max_length=50)
    car_cap = forms.IntegerField(label='car_cap')
    cigs = forms.BooleanField(label='cigs', required=False)
    pets = forms.BooleanField(label='pets', required=False)
    price = forms.FloatField(label='price')

class PassengerForm(forms.Form):
    start = forms.CharField(label='start', max_length=20)
    end = forms.CharField(label='end', max_length=20)
    date = forms.DateField(label='date', input_formats=['%d-%m-%Y', '%d/%m/%Y'])
    time_dep = forms.TimeField(label='time_dep')
    cigs = forms.BooleanField(label='cigs', required=False)
    pets = forms.BooleanField(label='pets', required=False)
    max_cost = forms.FloatField(label='max_cost')