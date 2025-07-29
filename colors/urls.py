from django.urls import path
from .views import GenerateColorView, color_count

urlpatterns = [
    path("generate/", GenerateColorView.as_view(), name="generate-color"),
    path("count/", color_count, name="color-count"),
]
