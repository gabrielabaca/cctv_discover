from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("map", views.cctv_map, name="cctv_map")
]