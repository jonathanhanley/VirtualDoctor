from django.shortcuts import render, HttpResponse
from datetime import datetime


# Create your views here.
def landing(request):
    return HttpResponse(f"UI {datetime.now()}")