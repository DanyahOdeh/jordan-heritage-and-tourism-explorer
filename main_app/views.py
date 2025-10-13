from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DestinationForm
from .models import Destination
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not (username and email and password and confirm_password):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        auth_login(request, user)
        return redirect('user_dashboard')

    return render(request, 'signup.html')

def about(request):
      return render(request, 'about.html')

def destination_list(request):
    destinations = Destination.objects.filter(status='approved')
    return render(request, 'destinations/list.html',{'destinations':destinations})

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    destination = get_object_or_404(Destination, pk=pk)
    return render(request, 'destinations/detail.html',{'destination': destination})

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.created_by = request.user  
            destination.status = 'pending'         
            destination.save()
            messages.success(request, 'Your destination has been submitted successfully and is pending approval!')
            return redirect('destination_list')
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        form = DestinationForm()

    return render(request, 'destinations/add.html', {'form': form})


def destination_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    destinations = Destination.objects.filter(status='approved')

    if query:
        destinations = destinations.filter(name__icontains=query)

    if category and category != 'all':
        destinations = destinations.filter(category=category)

    return render(request, 'destinations/list.html', {
        'destinations': destinations,
        'query': query,
        'selected_category': category,
    })

@login_required
def user_dashboard(request):
    """
    Displays the user's personal dashboard with their contributions and stats.
    """
    user = request.user

    user_destinations = Destination.objects.filter(created_by=user)
    approved_destinations_count = user_destinations.filter(status='approved').count()
    pending_destinations_count = user_destinations.filter(status='pending').count()
    total_destinations_count = user_destinations.count()

    latest_destinations = user_destinations.order_by('-created_at')[:3]

    context = {
        'user': user,
        'total_destinations_count': total_destinations_count,
        'approved_destinations_count': approved_destinations_count,
        'pending_destinations_count': pending_destinations_count,
        'latest_destinations': latest_destinations,
    }
    return render(request, 'userdashboard.html', context)