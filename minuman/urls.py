from django.urls import path
from minuman.views import show_minuman, show_minuman_by_id

urlpatterns = [
    path('', show_minuman, name='show_minuman'),
    path('<str:id>/', show_minuman_by_id, name='show_minuman_by_id'),
]
