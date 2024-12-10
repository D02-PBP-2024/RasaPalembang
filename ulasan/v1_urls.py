from django.urls import path
from ulasan.v1_views import ulasan_by_id

urlpatterns = [
    path("<uuid:id_ulasan>/", ulasan_by_id, name="ulasan_by_id"),
]
