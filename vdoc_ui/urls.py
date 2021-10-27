from django.urls import path, include

from vdoc_ui.views import landing

urlpatterns = [
    path('', landing , name="landing"),
]

