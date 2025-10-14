from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404 , HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import DeleteView


from django.contrib.auth.forms import UserCreationForm 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from .models import Destination , Review
from .forms import DestinationForm, ReviewForm



# Create your views here.
def home(request):
    return render(request, 'home.html')



def login(request):
    if request.method == 'POST':

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
            return redirect('login_url_name') 
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            
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
        return redirect('home')

    return render(request, 'signup.html')

def destination_list(request):
    destinations = Destination.objects.filter(status='approved')
    return render(request, 'destinations/list.html',{'destinations':destinations})

def destination_detail(request, pk):
    #destination = get_object_or_404(Destination, pk=pk, status='approved')
    destination = get_object_or_404(Destination, pk=pk)
    if destination.status != 'approved' and (not request.user.is_authenticated or destination.created_by != request.user):
    #return render(request, 'destinations/detail.html',{'destination': destination})
      raise Http404("No Destination matches the given query.")
    reviews = destination.reviews.all()
    review_form = ReviewForm()
    
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(destination=destination, user=request.user).exists()

    context = {
        'destination': destination,
        'reviews': reviews,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'destinations/detail.html', context)
@login_required
def add_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit = False)
            destination.created_by = request.user
            destination.save()
            messages.success(request, 'Destination submitted and will be shown when approved! ')
            #return redirect('destination_list')
            return redirect('destination_detail', pk= destination.pk)
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
    return render(request, 'destinations/add.html',{'form': form})
@login_required 
def edit_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    #authorization check only the creator can edit 
    if destination.created_by != request.user:
        messages.error(request,"You are not authorized to  edit this destination.")
        return redirect('destination_detail', pk=pk) 
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            edited_destination = form.save(commit=False)
            #sets status back to pending for admin approval 
            edited_destination.status ='pending' 
            edited_destination.save()
            messages.success(request, 'Destination updated and sent back for re-approval.') 
            return redirect('destination_detail',pk=pk)
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'destinations/edit.html', {'form': form, 'destination': destination})  
@login_required
def delete_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)

    if destination.created_by != request.user:
        messages.error(request,"You are not authorized to delete this destination.")
        return redirect('destination_detail', pk=pk)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, "Your destination successfully deleted.")
        return redirect('destination_list')
    
    return render(request, 'destinations/confirm_delete.html', {'destination': destination})

class AddReviewView(LoginRequiredMixin, View):
    #Handles displaying and the submission for adding a review
    def post(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        form = ReviewForm(request.POST)

        if form.is_valid():
            if Review.objects.filter(destination = destination, user=request.user).exists():
                messages.error(request, "You have already reviewed this destination.")
            else:
                review = form.save(commit=False)
                review.destination = destination
                review.user = request.user 
                review.save()  
                messages.success(request, "Your review has been added.")
        else:
            messages.error(request, "Error submitting your review. try again")
        return HttpResponseRedirect(destination.get_absolute_url() if hasattr(destination, 'get_absolute_url') else reverse('destination_detail', args=[pk]))             
class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        return self.request.user == review.user

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        destination_pk = review.destination.pk
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('destination_detail', pk=destination_pk)
