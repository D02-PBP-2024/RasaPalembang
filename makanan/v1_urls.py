from django.urls import path
from makanan.v1_views import makanan, makanan_by_id, kategori_list
from favorit.v1_views import favorit_by_makanan

app_name = "v1_makanan"

urlpatterns = [
    path("", makanan, name="makanan"),
    path("<uuid:id_makanan>/", makanan_by_id, name="makanan_by_id"),
    path("<uuid:id_makanan>/favorit/", favorit_by_makanan, name="favorit_by_makanan"),
    path('kategori/', kategori_list, name='kategori_list'),
]
