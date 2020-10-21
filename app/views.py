""" app/views.py """
from django.shortcuts import HttpResponse
# Create your views here.


def index(request):
    """function index"""
    return HttpResponse("Hello world")
