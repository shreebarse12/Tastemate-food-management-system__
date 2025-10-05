
# menu/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Dish(models.Model):
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    MEAL_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    canteen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_veg = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    served_date = models.DateField(default=timezone.localdate)  # default to today
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-served_date', 'meal_type', 'name']

    def __str__(self):
        return f"{self.name} — {self.canteen.username}"
