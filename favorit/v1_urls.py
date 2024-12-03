from django.urls import path
from favorit.v1_views import api_show_favorit, api_favorit_detail, api_add_makanan_to_favorites, api_add_minuman_to_favorites, api_add_restoran_to_favorites

app_name = "v1_favorit"

urlpatterns = [
    path("", api_show_favorit, name="api_show_favorit"),
    path("<uuid:favorit_id>/", api_favorit_detail, name="api_favorit_detail"),
    path("makanan/<uuid:item_id>/favorit/", api_add_makanan_to_favorites, name="api_add_makanan_to_favorites"),
    path("minuman/<uuid:item_id>/favorit/", api_add_minuman_to_favorites, name="api_add_minuman_to_favorites"),
    path("restoran/<uuid:item_id>/favorit/", api_add_restoran_to_favorites, name="api_add_restoran_to_favorites"),
]
