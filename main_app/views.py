from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DestinationForm
from .models import Destination

# Create your views here.
def home(request):
    return render(request, 'home.html')

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
            destination.created_by = request.user 
            destination.save()
            return redirect('destination_list')
        else:
            form = DestinationForm()

        return render(request, 'destinations/add.html',{'form': form})
        