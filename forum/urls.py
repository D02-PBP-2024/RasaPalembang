from django.urls import path
from forum.views import show_forum, balas, show_forum_by_id, create_forum

app_name = "forum"

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('<uuid:id>/', show_forum_by_id, name='show_forum_by_id'),
    path('<uuid:id>/balas', balas, name='balas'),
    path('create/', create_forum, name='create_forum'),
]