from django.shortcuts import render, HttpResponse
from datetime import datetime, timedelta


# Create your views here.
def landing(request):
    return HttpResponse(f"UI {datetime.now() + timedelta(hours=1)}")