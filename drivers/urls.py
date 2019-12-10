from django.urls import path
from django.urls import path, include

from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profil'),
    path('signup/', views.signup_view, name='rejestracja'),
    path('home/', views.home_view, name='home'),
    path('add_driver/', views.add_driver_view, name='dodaj przejazd'),
    path('add_passenger/', views.add_passenger_view, name='dodaj przejazd'),
    path('', views.home_view, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('edit_driver/<int:id>', views.edit_driver_ride_view, name='edit_driver')
]