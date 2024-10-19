from django.urls import path
from restoran.views import *

urlpatterns = [
    path('restoran', show_restoran, name='show_restoran'),
    path('create-restoran/', create_restoran, name='create_restoran'),
    path('edit-restoran/<uuid:id>', edit_restoran, name='edit_restoran'),
    path('delete-restoran/<uuid:id>', delete_restoran, name='delete_restoran'),
]