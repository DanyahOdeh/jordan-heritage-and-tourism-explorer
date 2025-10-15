from django import forms
from .models import Destination, Review
from django.contrib.auth.models import User

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name','description','category','location','activity_type','image']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control dropdown-align'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_type': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices = [(i, str(i)) for i in range(1,6)],
        widget = forms.RadioSelect,
        label = 'Your Rating (1-5 Stars)',
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }   

   