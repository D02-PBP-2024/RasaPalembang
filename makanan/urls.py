from django.urls import path
from makanan.views import *

app_name = 'makanan'

urlpatterns = [
    path('', show_makanan, name='show_makanan'),
    path('create/', create_makanan, name='create_makanan'),
    path('makanan/<uuid:id>/', show_makanan_by_id, name='show_makanan_by_id')
    
]