from django.urls import path
from django.urls import path, include

from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profil'),
    path('delete_passenger/<int:id>', views.delete_passenger_view, name='delete_passenger'),
    path('ride_chat/<int:id>', views.ride_chat_view, name='ride_chat'),
    path('signup/', views.signup_view, name='rejestracja'),
    path('home/', views.home_view, name='home'),
    path('add_driver/', views.add_driver_view, name='add_driver'),
    path('add_passenger/', views.add_passenger_view, name='add_passenger'),
    path('', views.home_view, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('edit_driver/<int:id>', views.edit_driver_ride_view, name='edit_driver'),
    path('edit_passenger/<int:id>', views.edit_passenger_ride_view, name='edit_passenger'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('delete_driver/<int:id>', views.delete_driver_view, name='delete_driver'),
    path('delete_p_ride/<int:id>', views.delete_p_ride_view, name='delete_p_ride'),
    path('delete_d_ride/<int:id>', views.delete_d_ride_view, name='delete_d_ride'),
    
]