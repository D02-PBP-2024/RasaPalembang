from ulasan.views import ulasan, tambah_ulasan, hapus_ulasan
from django.urls import path
from restoran.views import *


app_name = "ulasan"

urlpatterns = [
    path("", ulasan, name="ulasan"),
    path("tambah/", tambah_ulasan, name="tambah_ulasan"),
    path("hapus/", hapus_ulasan, name="hapus_ulasan"),
]
