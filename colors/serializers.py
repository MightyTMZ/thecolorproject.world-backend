from rest_framework import serializers
from .models import Color
from django.core.validators import MinValueValidator, MaxValueValidator

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['hex_code', 'r', 'g', 'b', 'created_at', 'times_discovered']
        read_only_fields = ['created_at', 'times_discovered']

    def validate(self, data):
        for channel in ['r', 'g', 'b']:
            value = data.get(channel)
            if value is None or not (0 <= value <= 255):
                raise serializers.ValidationError(f"{channel} must be between 0 and 255")
        return data
