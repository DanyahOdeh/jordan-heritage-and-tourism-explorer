from django.urls import path
from . import views # Import views to connect routes to view functions
from .views import AddReviewView, DeleteReviewView
urlpatterns = [
    # Routes will be added here
     path('', views.home, name='home'),
     
    # Destination URLs
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/add/', views.add_destination, name='add_destination'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'), 
    path('destinations/<int:pk>/edit/', views.edit_destination, name='edit_destination'),
    path('destinations/<int:pk>/delete/', views.delete_destination, name='delete_destination'),
    path('destinations/<int:pk>/review/add/', AddReviewView.as_view(), name='add_review'),
    path('reviews/<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    #  path('accounts/signup/', views.signup, name='signup'),
]