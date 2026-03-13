from django.urls import path
from django.http import JsonResponse


def healthcheck(_request):
    return JsonResponse({"status": "ok", "scope": "public"})


urlpatterns = [
    path("health/", healthcheck, name="public-health"),
]
