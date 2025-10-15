from django.urls import path
from . import views 
from .views import AddReviewView, DeleteReviewView
from django.contrib.auth import views as auth_views 
from django.urls import path, reverse_lazy 
urlpatterns = [
    # Routes will be added here
    path('', views.home, name='home'),  
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/add/', views.add_destination, name='add_destination'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'), 
    path('destinations/<int:pk>/edit/', views.edit_destination, name='edit_destination'),
    path('destinations/<int:pk>/delete/', views.delete_destination, name='delete_destination'),
    path('destinations/<int:pk>/review/add/', AddReviewView.as_view(), name='add_review'),
    path('reviews/<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='accounts_login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('user-dashboard/<int:user_id>', views.user_dashboard, name='user_dashboard'),
    path('account/manage/', views.manage_account, name='manage_account'),
    path('account/delete/', views.delete_account, name='delete_account'), 


]