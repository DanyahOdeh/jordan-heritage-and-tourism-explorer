from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
     path('', views.home, name='home'),
     path('login/', views.login, name='login')
    #  path('accounts/signup/', views.signup, name='signup'),
]