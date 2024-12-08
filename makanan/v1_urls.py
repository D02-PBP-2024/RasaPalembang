from django.urls import path
from makanan.v1_views import makanan, makanan_by_id

app_name = "v1_makanan"

urlpatterns = [
    path("", makanan, name="makanan"),
    path("<uuid:id_makanan>/", makanan_by_id, name="makanan_by_id"),
]
