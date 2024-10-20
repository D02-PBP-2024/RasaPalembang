from django.urls import path
from makanan.views import *

app_name = 'makanan'

urlpatterns = [
    path('', show_makanan, name='show_makanan'),
    path('tambah/', tambah_makanan, name='tambah_makanan'),
    path('<uuid:id>/', show_makanan_by_id, name='show_makanan_by_id'),
    path('<uuid:id>/edit/', edit_makanan, name='edit_makanan'),
    path('<uuid:id>/delete/', delete_makanan, name='delete_makanan'),
]