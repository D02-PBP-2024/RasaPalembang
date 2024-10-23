from django.urls import path
from restoran.views import *


app_name = "restoran"

urlpatterns = [
    path('', restoran, name='restoran'),
    path('tambah/', tambah_restoran, name='tambah'),
    path('ubah/<uuid:id>', ubah_restoran, name='ubah'),
    path('hapus/<uuid:id>', hapus_restoran, name='hapus'),
    path('detail/<uuid:id>', lihat_restoran, name='detail'), 
]
