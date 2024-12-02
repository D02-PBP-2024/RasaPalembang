from django.urls import path
from restoran.v1_views import minuman_by_restoran

app_name = "v1_restoran"

urlpatterns = [
    path("<uuid:id_restoran>/minuman/", minuman_by_restoran, name="minuman_by_restoran"),
]
