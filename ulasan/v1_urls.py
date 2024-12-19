from ulasan.v1_views import ulasan_by_id, ulasan_by_username
from django.urls import path

urlpatterns = [
    path("<uuid:id_ulasan>/", ulasan_by_id, name="ulasan_by_id"),
    path("profile/<slug:username>/", ulasan_by_username, name="ulasan_by_username"),
]
