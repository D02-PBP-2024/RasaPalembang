from django.urls import path
from favorit.v1_views import favorit, favorit_by_id, makanan_by_id_favorit, minuman_by_id_favorit, restoran_by_id_favorit

app_name = "v1_favorit"

urlpatterns = [
    path("", favorit, name="favorit"),
    path("<uuid:id_favorit>/", favorit_by_id, name="favorit_by_id"),
    path("makanan/<uuid:id_makanan>/favorit/", makanan_by_id_favorit, name="makanan_by_id_favorit"),
    path("minuman/<uuid:id_minuman>/favorit/", minuman_by_id_favorit, name="minuman_by_id_favorit"),
    path("restoran/<uuid:id_restoran>/favorit/", restoran_by_id_favorit, name="restoran_by_id_favorit"),
]
