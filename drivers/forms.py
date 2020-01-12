from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Imię')
    last_name = forms.CharField(max_length=100, help_text='Nazwisko')
    email = forms.EmailField(max_length=150, help_text='Adres email')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        
        self.fields['username'].help_text = 'Nazwa użytkownika'
        self.fields['password1'].help_text = 'Hasło'
        self.fields['password2'].help_text = 'Powtórz hasło'

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, help_text='Imię')
    last_name = forms.CharField(max_length=100, help_text='Nazwisko')
    email = forms.EmailField(max_length=150, help_text='Adres email')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, c_user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.c_user = c_user 
        self.fields['username'].help_text = 'Nazwa użytkownika'

    def clean_email(self):
        username = self.c_user
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email




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
    start = forms.CharField(label='start', max_length=20, help_text='Skąd jedziesz')
    end = forms.CharField(label='end', max_length=20, help_text='Dokąd')
    date = forms.DateField(label='date', input_formats=['%d-%m-%Y', '%d/%m/%Y'], help_text='Kiedy [Dzień/Miesiąc/Rok]')
    time_dep = forms.TimeField(label='time_dep', help_text='O której chcesz wyjechać')
    cigs = forms.BooleanField(label='cigs', required=False, help_text='Zaznacz jeśli chcesz palić papierosy w samochodzie')
    pets = forms.BooleanField(label='pets', required=False, help_text='Zaznacz jeśli jedziesz ze zwierzęciem')
    max_cost = forms.FloatField(label='max_cost', help_text='Ile możesz maksymalnie zapłacić')

class MessageForm(forms.Form):
    message = forms.CharField(label='message', max_length=1000)
