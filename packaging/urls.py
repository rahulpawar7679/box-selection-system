from django.urls import path
from .views import recommend_box_view, list_boxes_view

urlpatterns = [
    path('boxes/', list_boxes_view, name='list-boxes'),
    path('recommend-box/', recommend_box_view, name='recommend-box'),
]