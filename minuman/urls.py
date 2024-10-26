from django.urls import path
from minuman.views import *

app_name = "minuman"

urlpatterns = [
    path("", show_minuman, name="show_minuman"),
    path("tambah/", tambah_minuman, name="tambah_minuman"),
    path("<uuid:id>/", detail_minuman, name="detail_minuman"),
    path("<uuid:id>/ubah/", ubah_minuman, name="ubah_minuman"),
    path("<uuid:id>/hapus/", hapus_minuman, name="hapus_minuman"),
    path("sorted/", show_minuman_by_sort, name="show_minuman_by_sort"),
]
