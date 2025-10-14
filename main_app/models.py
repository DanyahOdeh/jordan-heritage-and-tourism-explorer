from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 

class Destination(models.Model): 
    category_choice =[
        ('historical','Historical'),
        ('nature', 'Nature'),
        ('adventure', 'Adventure'),
    ] 

    status_choice = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('declined','Declined'), 
    ]

    name = models.CharField(max_length=200) 
    description = models.TextField()
    category= models.CharField(max_length=20, choices=category_choice) 
    location = models.CharField(max_length=100) 
    activity_type = models.CharField(max_length=100) 
    image = models.ImageField(upload_to = 'destinations/')
    created_at = models.DateTimeField(auto_now_add= True) 
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_des')
    status = models.CharField(max_length=10, choices=status_choice, default='pending') 

    def __str__(self): 
        return self.name
    def average_rating(self): 
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg']
    @property 
    def rating_display(self): 
        avg = self.average_rating()
        return f"{avg:.1f}/5" if avg else "N/A" 
    def __str__(self): return self.name 
    def get_absolute_url(self): return reverse("destination_detail", kwargs={"pk": self.pk}) 
    
class Review(models.Model):
        destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews') 
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_made') 
        #rating from 1 to 5 
        rating = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)]) 
        comment = models.TextField(blank=True) 
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta: 
            unique_together = ('destination', 'user') #order
            ordering= ['-created_at'] 
   
        def __str__(self): return f"Review by {self.user.username} for {self.destination.name}"