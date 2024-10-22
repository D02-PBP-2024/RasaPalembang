from django.urls import path
from makanan.views import *

app_name = 'makanan'

urlpatterns = [
    path('', show_makanan, name='show_makanan'),
    path('<uuid:id>/detail/', detail_makanan, name='detail_makanan'),
    path('tambah/', tambah_makanan, name='tambah_makanan'),
    path('<uuid:id>/edit/', edit_makanan, name='edit_makanan'),
    path('<uuid:id>/delete/', delete_makanan, name='delete_makanan'),
]