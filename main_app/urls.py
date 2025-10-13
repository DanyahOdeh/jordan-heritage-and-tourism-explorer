from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
     path('', views.home, name='home'),
     


    # Destination URLs
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/add/', views.add_destination, name='add_destination'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'), 
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    #  path('accounts/signup/', views.signup, name='signup'),
]


# from django.urls import path
# from . import views # Import views to connect routes to view functions
# from django.contrib.auth import views as auth_views # Import Django's auth views

# urlpatterns = [
#     # Home URL
#     path('', views.home, name='home'),
    
#     # User Authentication URLs (using Django's built-in views for better practice)
#     # Consider using Django's LoginView and LogoutView instead of custom ones for security and features
#     # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
#     # If you want to keep your custom login/signup:
#     path('login/', views.login_view, name='login'), # Your custom login view
#     path('signup/', views.signup_view, name='signup'), # Your custom signup view

#     # Destination URLs
#     path('destinations/', views.destination_list, name='destination_list'),
#     path('destinations/add/', views.add_destination, name='add_destination'),
#     path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'), 
    

#     path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
#     #  path('userdashboard/<int:user_id>/', views.user_dashboard, name='user_dashboard'),
# ]