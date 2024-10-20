from django.urls import path
from restoran.views import tambah_restoran

app_name = 'restoran'

urlpatterns = [
    path('', tambah_restoran, name='tambah_restoran'),
]
