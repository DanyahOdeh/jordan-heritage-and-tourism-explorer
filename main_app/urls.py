from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
     path('', views.home, name='home'),
    # Destination URLs
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/add/', views.add_destination, name='add_destination'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'), 
]