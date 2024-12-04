from django.urls import path
from forum.v1_views import forum_by_restoran
from minuman.v1_views import minuman_by_restoran
from restoran.v1_views import restoran, restoran_by_id, restoran_by_user

app_name = "v1_restoran"

urlpatterns = [
    path("<uuid:id_restoran>/minuman/", minuman_by_restoran, name="minuman_by_restoran"),
    path("<uuid:id_restoran>/forum/", forum_by_restoran, name="forum_by_restoran"),
    path("", restoran, name="restoran"),
    path("<uuid:id_restoran>/", restoran_by_id, name="restoran_by_id"),
    path("user/<str:username>/", restoran_by_user, name="restoran_by_user"),
]
