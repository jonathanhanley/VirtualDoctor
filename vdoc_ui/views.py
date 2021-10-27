from django.shortcuts import render, HttpResponse
from datetime import datetime, timedelta


# Create your views here.
def landing(request):
    return HttpResponse(f"Server Time {datetime.now() + timedelta(hours=0)}")