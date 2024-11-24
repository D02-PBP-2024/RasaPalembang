from django.urls import path
from minuman.v1_views import minuman, minuman_by_id

app_name = "v1_minuman"

urlpatterns = [
    path("", minuman, name="minuman"),
    path("<uuid:id>/", minuman_by_id, name="minuman_by_id"),
]
