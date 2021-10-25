from django.urls import path, reverse
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from vdoc_api.views import DeleteToken, APIUser

urlpatterns = [
    path('login/', obtain_auth_token, name="api-login"),
    path('logout/', DeleteToken.as_view(), name="api-logout"),
    path('user/', APIUser.as_view(), name="api-user"),
]

