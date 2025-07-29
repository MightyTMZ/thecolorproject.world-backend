from django.test import TestCase, Client
from django.urls import reverse
from .models import Color

class ColorModelTest(TestCase):
    def test_create_color(self):
        color = Color.objects.create(
            hex_code="#FF5733",
            r=255,
            g=87,
            b=51,
        )
        self.assertEqual(str(color), "#FF5733 (255, 87, 51)")
        self.assertEqual(color.times_discovered, 1)

    def test_color_hex_uniqueness(self):
        Color.objects.create(hex_code="#123456", r=18, g=52, b=86)
        with self.assertRaises(Exception):
            Color.objects.create(hex_code="#123456", r=18, g=52, b=86)

class ColorEndpointTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.color_data = {
            "hex_code": "#ABCDEF",
            "r": 171,
            "g": 205,
            "b": 239
        }

    def test_create_color_endpoint(self):
        response = self.client.post(
            reverse("generate-color"), 
            data=self.color_data, 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Color.objects.count(), 1)

    def test_duplicate_color_submission(self):
        self.client.post(reverse("generate-color"), data=self.color_data, content_type="application/json")
        response = self.client.post(reverse("generate-color"), data=self.color_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Color.objects.first().times_discovered, 2)

    def test_color_count_endpoint(self):
        for i in range(5):
            Color.objects.create(hex_code=f"#AAAAA{i}", r=i, g=i, b=i)
        response = self.client.get(reverse("color-count"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_colors_discovered'], 5)
