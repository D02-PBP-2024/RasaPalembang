from minuman.v1_views import minuman, minuman_by_id
from favorit.v1_views import favorit_by_minuman
from django.urls import path

app_name = "v1_minuman"

urlpatterns = [
    path("", minuman, name="minuman"),
    path("<uuid:id_minuman>/", minuman_by_id, name="minuman_by_id"),
    path("<uuid:id_minuman>/favorit/", favorit_by_minuman, name="favorit_by_minuman"),
]
