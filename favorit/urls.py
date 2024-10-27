from django.urls import path
from favorit.views import show_favorit, ubah_favorit, hapus_favorit, add_to_favorites

app_name = "favorit"

urlpatterns = [
    path("", show_favorit, name="show_favorit"),  # Menampilkan daftar favorit
    path("ubah/<uuid:favorit_id>/", ubah_favorit, name="ubah_favorit"),  # Mengedit favorit
    path("hapus/<uuid:favorit_id>/", hapus_favorit, name="hapus_favorit"),  # Menghapus favorit
    path('tambah/<str:item_type>/<uuid:item_id>/', add_to_favorites, name='add_to_favorites'), # menambahkan item ke favorit
]
