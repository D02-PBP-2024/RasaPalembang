from django.urls import path
from makanan.views import *

app_name = "makanan"

urlpatterns = [
    path("", show_makanan, name="show_makanan"),
    path("tambah/", tambah_makanan, name="tambah_makanan"),
    path("<uuid:id>", detail_makanan, name="detail_makanan"),
    path("<uuid:id>/ubah/", ubah_makanan, name="ubah_makanan"),
    path("<uuid:id>/hapus/", hapus_makanan, name="hapus_makanan"),
    path(
        "filter_makanan_by_kategori/",
        filter_by_kategori,
        name="filter_makanan_by_kategori",
    ),
]
