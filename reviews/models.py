from django.db import models
from django.conf import settings

class Review(models.Model):
    # The student who writes the review
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Student'},
        related_name='reviews_made',
        null=True,   # temporarily allow NULL
        blank=True
    )

    # The canteen being reviewed
    canteen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Canteen'},
        related_name='reviews_received',
        null=True,   # temporarily allow NULL
        blank=True
    )

    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        null=True,   # temporarily allow NULL
        blank=True,
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        student_name = self.student.username if self.student else "Unknown"
        canteen_name = self.canteen.canteen_name if self.canteen else "Unknown"
        return f"{student_name} → {canteen_name} ({self.rating}/5)"
