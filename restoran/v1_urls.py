from django.urls import path
from makanan.v1_views import makanan_by_restoran
from minuman.v1_views import minuman_by_restoran
from restoran.v1_views import restoran, restoran_by_id, restoran_by_user, get_user_flutter
from ulasan.v1_views import ulasan_by_restoran
from forum.v1_views import forum_by_restoran
from favorit.v1_views import favorit_by_restoran

app_name = "v1_restoran"

urlpatterns = [
    path("", restoran, name="restoran"),
    path("<uuid:id_restoran>/", restoran_by_id, name="restoran_by_id"),
    path("user/<str:username>/", restoran_by_user, name="restoran_by_user"), # should not exist, wrong implementation
    path("<uuid:id_restoran>/makanan/", makanan_by_restoran, name="makanan_by_restoran"),
    path("<uuid:id_restoran>/minuman/", minuman_by_restoran, name="minuman_by_restoran"),
    path("<uuid:id_restoran>/favorit/", favorit_by_restoran, name="favorit_by_restoran"),
    path("<uuid:id_restoran>/forum/", forum_by_restoran, name="forum_by_restoran"),
    path("<uuid:id_restoran>/ulasan/", ulasan_by_restoran, name="ulasan_by_restoran"),
    path('get_user_flutter/', get_user_flutter, name='get_user_flutter'),
]
