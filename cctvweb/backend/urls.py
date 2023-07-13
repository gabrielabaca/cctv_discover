from django.urls import path

from . import views

urlpatterns = [
    path("get_markets", views.get_markets, name="get_market"),
    path("get_snap/<device_uuid>", views.get_snapshot, name="get_snap"),
    path("test_shodan", views.test_shodan)
]