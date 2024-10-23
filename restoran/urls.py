from django.urls import path
from restoran.views import *


app_name = "restoran"

urlpatterns = [
    path('', restoran, name='restoran'),
    path('tambah/', tambah_restoran, name='tambah'),
    path('<uuid:id>/edit', ubah_restoran, name='ubah'),
    path('<uuid:id>/delete', hapus_restoran, name='hapus'),
    path('<uuid:id>', lihat_restoran, name='detail'), 
]
