from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from .services.shodanServices import Shodan

## Services
from .services.devicesServices import DevicesServices

## Extras 
from uuid import UUID
# Create your views here.

def get_markets(request:HttpRequest):
    if request.method == "GET":
        return DevicesServices().get_devices()
    

def get_snapshot(request:HttpRequest, device_uuid:UUID):
    if request.method == "GET":
        return DevicesServices().get_snapshop(device_uuid)
    

def test_shodan(request:HttpRequest):
    if request.method == "GET":
        return DevicesServices().fetch_devices('azWuOwkubwNGb17Wpc2WZzUTXQwywzUN', '746-550a95c4')
