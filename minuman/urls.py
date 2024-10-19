import uuid
from django.urls import path
from minuman.views import show_minuman, create_minuman, show_minuman_by_id, edit_minuman, delete_minuman

app_name = 'minuman'

urlpatterns = [
    path('', show_minuman, name='show_minuman'),
    path('create/', create_minuman, name='create_minuman'),
    path('<uuid:id>/', show_minuman_by_id, name='show_minuman'),
    path('<uuid:id>/edit', edit_minuman, name='edit_minuman'),
    path('<uuid:id>/delete', delete_minuman, name='delete_minuman'),
]
