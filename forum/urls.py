from django.urls import path
from forum.views import show_forum, balas, show_forum_by_id, create_forum, delete_forum, delete_balasan, edit_balasan, edit_forum, vote_balasan, balasan_by_id

app_name = "forum"

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('<uuid:id_forum>/', show_forum_by_id, name='show_forum_by_id'),
    path('<uuid:id_forum>/balas', balas, name='balas'),
    path('tambah/', create_forum, name='create_forum'),
    path('<uuid:id_forum>/delete_balasan/<uuid:id_balasan>', delete_balasan, name='delete_balasan'),
    path('<uuid:id_forum>/delete_forum', delete_forum, name='delete_forum'),
    path('<uuid:id_forum>/edit_balasan/<uuid:id_balasan>', edit_balasan, name='edit_balasan'),
    path('<uuid:id_forum>/edit_forum', edit_forum, name="edit_forum"),
    path('<uuid:id_forum>/vote-balasan/<uuid:id_balasan>', vote_balasan, name='vote_balasan'),
    # path('<uuid:id_forum>/<uuid:id_balasan>', balasan_by_id, name='balasan_by_id'),
]