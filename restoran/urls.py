from django.urls import path, include
from restoran.views import *

app_name = "restoran"

urlpatterns = [
    path("", show_restoran, name="show_restoran"),
    path("tambah/", tambah_restoran, name="tambah_restoran"),
    path("<uuid:id>/", lihat_restoran, name="detail_restoran"),
    path("<uuid:id>/ubah/", ubah_restoran, name="ubah_restoran"),
    path("<uuid:id>/hapus/", hapus_restoran, name="hapus_restoran"),
    path("<uuid:id>/ulasan/", include("ulasan.urls")),
    path('sort/', sort_restoran, name='sort_restoran'),
    path('create/', create_restoran_flutter, name='create_restoran'),
]
