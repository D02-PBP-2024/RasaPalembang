from django.urls import path
from makanan.views import *

app_name = 'makanan'

urlpatterns = [
    path('', show_makanan, name='show_makanan'),
    path('<uuid:id>/', show_makanan_by_id, name='show_makanan_by_id'),
    path('tambah/', tambah_makanan, name='tambah_makanan'),
    path('<uuid:id>/edit/', edit_makanan, name='edit_makanan'),
    path('<uuid:id>/delete/', delete_makanan, name='delete_makanan'),
    path('kategori/', show_kategori, name='show_kategori'),
    path('kategori/tambah/', tambah_kategori, name='tambah_kategori'),
    path('kategori/<uuid:id>/edit/', edit_kategori, name='edit_kategori'),
    path('kategori/<uuid:id>/delete/', delete_kategori, name='delete_kategori'),
]