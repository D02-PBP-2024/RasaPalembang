from django.urls import path
from restoran.v1_views import restoran, restoran_by_id, restoran_by_user

app_name = "v1_restoran"

urlpatterns = [
    path("", restoran, name="restoran"),
    path("<uuid:id_restoran>/", restoran_by_id, name="restoran_by_id"),
    path("user/<str:username>/", restoran_by_user, name="restoran_by_user"),
]
