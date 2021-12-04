from django.urls import path, reverse
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from vdoc_api.views import DeleteToken, APIUser, APIConsultant, APIQuestionSet, APIQuestion, APIAnswer, IsConsultant

urlpatterns = [
    path('login/', obtain_auth_token, name="api-login"),
    path('logout/', DeleteToken.as_view(), name="api-logout"),
    path('user/', APIUser.as_view(), name="api-user"),
    path('consultant/', APIConsultant.as_view(), name="api-consultant"),
    path('question-set/', APIQuestionSet.as_view(), name="api-question-set"),
    path('question/', APIQuestion.as_view(), name="api-question"),
    path('answer/', APIAnswer.as_view(), name="api-answer"),
    path('is-consultant/', IsConsultant.as_view(), name="api-is-consultant"),
]

