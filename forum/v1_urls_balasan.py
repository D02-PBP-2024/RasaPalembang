from django.urls import path
from forum.v1_views import balasan_by_id

app_name = "v1_balasan"

urlpatterns = [
    path("<uuid:id_balasan>/", balasan_by_id, name="balasan_by_id"),
]