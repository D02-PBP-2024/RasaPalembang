from django.urls import path
from restoran.views import *


app_name = "restoran"

urlpatterns = [
    path('', restoran, name='restoran'),
    path('tambah/', tambah_restoran, name='tambah'),
    path('ubah/<uuid:id>', ubah_restoran, name='ubah'),
    path('hapus/<uuid:id>', hapus_restoran, name='hapus'),
    path('view-restoran/<uuid:id>', view_restoran, name='view_restoran'), 
]
