from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CANTEEN = 'Canteen'
    STUDENT = 'Student'
    ROLE_CHOICES = [
        (CANTEEN, 'Canteen'),
        (STUDENT, 'Student'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True, help_text="Full address of the canteen")
    canteen_name = models.CharField(max_length=150, blank=True)
    
    # --- NEW FIELDS TO ADD ---
    # These will store the geographic coordinates for each canteen.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    # --- END OF NEW FIELDS ---

    def is_canteen(self):
        return self.role == self.CANTEEN

    def is_student(self):
        return self.role == self.STUDENT

    def clean(self):
        super().clean()

        # Validation for canteen role
        if self.role == self.CANTEEN and not self.canteen_name:
            raise ValidationError("Canteen name is required for Canteen users.")

        # If student, always clear canteen_name
        if self.role == self.STUDENT:
            self.canteen_name = ""

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
