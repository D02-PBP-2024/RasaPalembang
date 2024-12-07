from django.urls import path
from minuman.v1_views import minuman, minuman_by_id, favorit_by_minuman

app_name = "v1_minuman"

urlpatterns = [
    path("", minuman, name="minuman"),
    path("<uuid:id_minuman>/", minuman_by_id, name="minuman_by_id"),
    path("minuman/<uuid:id_minuman>/favorit/", favorit_by_minuman, name="favorit_by_minuman"),
]
