from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from .forms import DestinationForm, ReviewForm, UserUpdateForm 
from .models import Destination, Review
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout




# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            # ✅ redirect with ID in the URL
            return redirect('user_dashboard', user_id=user.id)
        else:
            context = {'error_message': 'Invalid username or password.'}
            return render(request, 'registration/login.html', context)

    return render(request, 'registration/login.html', {'error_message': error_message})


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
        return redirect('user_dashboard',user_id=user.id)

    return render(request, 'signup.html')

def about(request):
      return render(request, 'about.html')

def destination_list(request):
    destinations = Destination.objects.filter(status='approved')
    return render(request, 'destinations/list.html',{'destinations':destinations})

@login_required
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
            destination = form.save(commit=False)
            destination.created_by = request.user  
            destination.status = 'pending'         
            destination.save()
            messages.success(request, 'Your destination has been submitted successfully and is pending approval!')
            return redirect('user_dashboard',  user_id=request.user.id)
            # return redirect('destination_detail', pk= destination.pk)
        else:
            messages.error(request, 'Please check the form for errors.')
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

@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user_destinations = Destination.objects.filter(created_by=user)
    approved_destinations_count = user_destinations.filter(status='approved').count()
    pending_destinations_count = user_destinations.filter(status='pending').count()
    total_destinations_count = user_destinations.count()
    latest_destinations = user_destinations.order_by('-created_at')[:3]

   
    user_reviews = Review.objects.filter(user=user).order_by('-created_at')
    user_reviews_count = user_reviews.count()
    latest_reviews = user_reviews[:3]

    total_feedback_count = user_reviews_count 

    context = {
        'user': user,
        'total_destinations_count': total_destinations_count,
        'approved_destinations_count': approved_destinations_count,
        'pending_destinations_count': pending_destinations_count,
        'latest_destinations': latest_destinations,
        'user_reviews_count': user_reviews_count,
        'total_feedback_count': total_feedback_count,
        'latest_reviews': latest_reviews,  
    }
    return render(request, 'userdashboard.html', context)



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


@login_required
def manage_account(request):
    user = request.user 

    
    if 'update_info' in request.POST:
        info_form = UserUpdateForm(request.POST, instance=user)
        if info_form.is_valid():
            info_form.save()
            messages.success(request, 'Your account information has been updated successfully!')
            return redirect('manage_account') 
        else:
            messages.error(request, 'Error updating account information. Please review the fields.')
    else:
        info_form = UserUpdateForm(instance=user)

    
    if 'change_password' in request.POST:
        password_form = PasswordChangeForm(user=user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('manage_account')
        else:
            messages.error(request, 'Error changing password. Please ensure your old password is correct.')
    else:
        password_form = PasswordChangeForm(user=user)

    context = {
        'info_form': info_form,
        'password_form': password_form,
    }
    return render(request, 'manage_account.html', context)      


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        
        logout(request) 
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home') 

    return redirect('manage_account')