from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DestinationForm
from .models import Destination

# Create your views here.
def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User # إذا كنت ستستخدم نظام المستخدمين المدمج في Django
from django.contrib.auth.forms import UserCreationForm # بديل أبسط

def login(request):
    if request.method == 'POST':
        # هنا يمكنك معالجة بيانات النموذج
        # مثال بسيط لإنشاء مستخدم (للتوضيح فقط، استخدم نماذج Django forms.py للإنتاج)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        terms_accepted = request.POST.get('terms_accepted')

        if not (username and email and password and terms_accepted):
            messages.error(request, 'Please fill in all fields and accept the terms.')
            return render(request, 'login.html')

        try:
            # مثال لإنشاء مستخدم جديد
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login_url_name') # قم بتوجيه المستخدم لصفحة تسجيل الدخول
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            # يمكنك إضافة معالجة للأخطاء مثل اسم المستخدم موجود مسبقًا
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
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')

    return render(request, 'signup.html')

def destination_list(request):
    destinations = Destination.objects.filter(status='approved')
    return render(request, 'destinations/list.html',{'destinations':destinations})

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    destination = get_object_or_404(Destination, pk=pk)
    return render(request, 'destinations/detail.html',{'destination': destination})

@login_required
def add_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit = False)
            #destination.created_by = request.user
            destination.save()
            return redirect('destination_list')
    else:
            form = DestinationForm()
    return render(request, 'destinations/add.html',{'form': form})

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
