
from django.contrib import admin
from .models import Dish

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "meal_type", "price", "canteen", "served_date", "available")
    list_filter = ("meal_type", "available", "served_date")
    search_fields = ("name", "canteen__username")
