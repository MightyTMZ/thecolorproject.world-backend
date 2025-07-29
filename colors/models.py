from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Color(models.Model):
    hex_code = models.CharField(max_length=7, unique=True)
    r = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)]
    )
    g = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)]
    )
    b = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    times_discovered = models.PositiveIntegerField(default=1)


    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-times_discovered']),
        ]


    def __str__(self):
        return f"{self.hex_code} ({self.r}, {self.g}, {self.b})"