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
    start = forms.CharField(label='start', max_length=20, help_text='Skąd jedziesz')
    end = forms.CharField(label='end', max_length=20, help_text='Dokąd')
    stops = forms.CharField(label='stops', max_length=100, required=False, help_text='Gdzie możesz się zatrzymać')
    date = forms.DateField(label='date', input_formats=['%d-%m-%Y', '%d/%m/%Y'], help_text='Kiedy [Dzień/Miesiąc/Rok]')
    time_dep = forms.TimeField(label='time_dep', help_text='O której godzinie wyjeżdżasz')
    car_model = forms.CharField(label='car_model', max_length=50, help_text='Jakim autem')
    car_cap = forms.IntegerField(label='car_cap', help_text='Ilu możesz zabrać pasażerów')
    cigs = forms.BooleanField(label='cigs', required=False, help_text='Zaznacz jeśli nie pozwalasz palić papierosów w samochodzie')
    pets = forms.BooleanField(label='pets', required=False, help_text='Zaznacz jeśli nie chcesz przewozić zwierząt')
    price = forms.FloatField(label='price', help_text='Cena od kilometra')

class PassengerForm(forms.Form):
    start = forms.CharField(label='start', max_length=20)
    end = forms.CharField(label='end', max_length=20)
    date = forms.DateField(label='date', input_formats=['%d-%m-%Y', '%d/%m/%Y'])
    time_dep = forms.TimeField(label='time_dep')
    cigs = forms.BooleanField(label='cigs', required=False)
    pets = forms.BooleanField(label='pets', required=False)
    max_cost = forms.FloatField(label='max_cost')