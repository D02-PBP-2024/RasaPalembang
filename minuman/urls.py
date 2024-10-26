from django.urls import path
from minuman.views import *

app_name = "minuman"

urlpatterns = [
    path("", show_minuman, name="show_minuman"),
    path("tambah/", tambah_minuman, name="tambah_minuman"),
    path("<uuid:id>/", detail_minuman, name="detail_minuman"),
    path("<uuid:id>/edit/", edit_minuman, name="edit_minuman"),
    path("<uuid:id>/delete/", delete_minuman, name="delete_minuman"),
    path("sorted/", show_minuman_by_sort, name="show_minuman_by_sort"),
]
