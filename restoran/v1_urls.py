from django.urls import path
from forum.v1_views import forum_by_restoran
from minuman.v1_views import minuman_by_restoran

app_name = "v1_restoran"

urlpatterns = [
    path("<uuid:id_restoran>/minuman/", minuman_by_restoran, name="minuman_by_restoran"),
    path("<uuid:id_restoran>/forum/", forum_by_restoran, name="forum_by_restoran")
]
