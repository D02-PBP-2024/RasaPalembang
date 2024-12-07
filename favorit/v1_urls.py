from django.urls import path
from favorit.v1_views import favorit, favorit_by_id, favorit_by_makanan

app_name = "v1_favorit"

urlpatterns = [
    path("", favorit, name="favorit"),
    path("<uuid:id_favorit>/", favorit_by_id, name="favorit_by_id"),
    path("makanan/<uuid:id_makanan>/favorit/", favorit_by_makanan, name="favorit_by_makanan"),

]
