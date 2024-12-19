from django.urls import path
from favorit.v1_views import favorit, favorit_by_id

app_name = "v1_favorit"

urlpatterns = [
    path("", favorit, name="favorit"),
    path("<uuid:id_favorit>/", favorit_by_id, name="favorit_by_id"),
]
