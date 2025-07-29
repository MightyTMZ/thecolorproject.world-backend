from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Color
from .serializers import ColorSerializer
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.cache import cache_page


class GenerateColorView(APIView):
    def post(self, request):
        hex_code = request.data.get("hex_code")
        r = request.data.get("r")
        g = request.data.get("g")
        b = request.data.get("b")

        # Basic presence & type validation
        if not hex_code or r is None or g is None or b is None:
            return Response({"error": "hex_code, r, g, and b are all required."}, status=400)

        try:
            r = int(r)
            g = int(g)
            b = int(b)
        except ValueError:
            return Response({"error": "r, g, and b must be integers."}, status=400)

        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            return Response({"error": "RGB values must be between 0 and 255."}, status=400)

        # Create or update
        obj, created = Color.objects.get_or_create(
            hex_code=hex_code.upper(),
            defaults={"r": r, "g": g, "b": b}
        )

        if not created:
            Color.objects.filter(pk=obj.pk).update(times_discovered=F("times_discovered") + 1)
            obj.refresh_from_db()

        serializer = ColorSerializer(obj)
        return Response(
            {
                "status": "new" if created else "duplicate",
                "color": serializer.data,
            },
            status=status.HTTP_201_CREATED if created else 200,
        )

@cache_page(60)
def color_count(request):
    count = Color.objects.count()
    return JsonResponse({'total_colors_discovered': count})