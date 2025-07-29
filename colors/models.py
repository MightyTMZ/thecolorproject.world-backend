from django.db import models

class Color(models.Model):
    hex_code = models.CharField(max_length=7, unique=True)
    r = models.PositiveSmallIntegerField()
    g = models.PositiveSmallIntegerField()
    b = models.PositiveSmallIntegerField()    
    created_at = models.DateTimeField(auto_now_add=True)
    times_discovered = models.PositiveIntegerField(default=1)


    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-times_discovered']),
        ]


    def __str__(self):
        return f"{self.hex_code} ({self.r}, {self.g}, {self.b})"