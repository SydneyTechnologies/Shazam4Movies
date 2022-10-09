from django.urls import path
from django.shortcuts import HttpResponse
from .utils import ReadVideo

def test(request):
    ReadVideo()
    return HttpResponse("hello world!")

urlpatterns = [
    path("", test, name="test")
]