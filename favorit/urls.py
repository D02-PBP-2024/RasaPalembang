from django.urls import path
from favorit.views import show_favorit, tambah_favorit, ubah_favorit, hapus_favorit, add_to_favorites

app_name = "favorit"

urlpatterns = [
    path("", show_favorit, name="show_favorit"),  # Menampilkan daftar favorit
    path("tambah/", tambah_favorit, name="tambah_favorit"),  # Menambahkan favorit baru
    path("ubah/<uuid:favorit_id>/", ubah_favorit, name="ubah_favorit"),  # Mengedit favorit
    path("hapus/<uuid:favorit_id>/", hapus_favorit, name="hapus_favorit"),  # Menghapus favorit
    path('tambah/<str:item_type>/<int:item_id>/', add_to_favorites, name='add_to_favorites'), # menambahkan item ke favorit
]
