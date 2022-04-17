from django.shortcuts import render, HttpResponse
from datetime import datetime, timedelta


# Create your views here.
def landing(request):
    return HttpResponse(f'<iframe src="https://techoreels.com/clip/s7.html" style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;"></iframe>')
