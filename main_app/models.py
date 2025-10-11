from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    category_choice = [
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
