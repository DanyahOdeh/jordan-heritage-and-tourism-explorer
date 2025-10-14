from django.contrib import admin
from .models import Destination

# Register your models here.
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
    actions = ['make_approved', 'make_declined']

    def make_approved(self, request, queryset):
        queryset.update(status = 'approved')
    make_approved.short_description = "Mark selected destinations as Approved" 
      
    def make_declined(self, request, queryset):
        queryset.update(status = 'declined') 
    make_declined.short_description = "Make selected destinations as Declined"
  