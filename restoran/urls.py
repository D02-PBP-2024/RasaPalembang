from django.urls import path, include
from restoran.views import *


app_name = "restoran"

urlpatterns = [
    path('', restoran, name='restoran'),
    path('tambah/', tambah_restoran, name='tambah'),
    path('<uuid:id>/ubah/', ubah_restoran, name='ubah'),
    path('<uuid:id>/hapus/', hapus_restoran, name='hapus'),
    path('<uuid:id>/ulasan/', include('ulasan.urls')),
    path('<uuid:id>/', lihat_restoran, name='detail'), 
]
