from django.contrib import admin
from .models import Bike, Rental

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_available', 'hourly_rate')
    list_editable = ('is_available', 'hourly_rate')
    list_filter = ('is_available',)
    search_fields = ('name',)

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bike', 'start_time', 'end_time', 'total_fee')
    list_filter = ('start_time', 'bike__name')
    search_fields = ('user__username', 'bike__name')
