import uuid
from django.urls import path
from minuman.views import (
    show_minuman,
    tambah_minuman,
    show_minuman_by_id,
    edit_minuman,
    delete_minuman,
    show_minuman_by_sort,
)

app_name = "minuman"

urlpatterns = [
    path("", show_minuman, name="show_minuman"),
    path("tambah/", tambah_minuman, name="tambah_minuman"),
    path("<uuid:id>/", show_minuman_by_id, name="show_minuman_by_id"),
    path("<uuid:id>/edit/", edit_minuman, name="edit_minuman"),
    path("<uuid:id>/delete/", delete_minuman, name="delete_minuman"),
    path("sorted/", show_minuman_by_sort, name="show_minuman_by_sort"),
]
