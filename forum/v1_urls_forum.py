from django.urls import path
from forum.v1_views import forum_by_id, balasan_forum

app_name = "v1_forum"

urlpatterns = [
    path("<uuid:id_forum>/", forum_by_id, name="forum_by_id"),
    path("<uuid:id_forum>/balasan/", balasan_forum, name="balasan_forum"),
]