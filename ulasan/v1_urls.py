from django.urls import path
from ulasan.v1_views import ulasan_by_username, ulasan_by_id

urlpatterns = [
    path("<slug:username>/", ulasan_by_username, name="ulasan_by_username"),
    path("<uuid:id_ulasan>/", ulasan_by_id, name="ulasan_by_id"),
]
