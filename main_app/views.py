from django.shortcuts import render

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