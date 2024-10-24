from django.urls import path
from favorit.views import show_favorit, add_favorit, edit_favorit, delete_favorit

app_name = 'favorit'

urlpatterns = [
    path('', show_favorit, name='show_favorit'), # Menampilkan daftar favorit
    path('add/', add_favorit, name='add_favorit'),  # Menambahkan favorit baru
    path('edit/<uuid:favorit_id>/', edit_favorit, name='edit_favorit'),  # Mengedit favorit
    path('delete/<uuid:favorit_id>/', delete_favorit, name='delete_favorit'),  # Menghapus favorit
]
