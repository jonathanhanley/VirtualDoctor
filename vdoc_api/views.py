from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from vdoc_api.custom_permissions import UserPermissions
from vdoc_api.serializers import UserSerializer

User = get_user_model()

class DeleteToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        token = Token.objects.filter(user=user)
        token.delete()
        return Response({'message': 'Logged out'})


class APIUser(APIView):
    permission_classes = [UserPermissions]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        username = email
        if not email:
            return Response(data={"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response(data={"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username) or User.objects.filter(username=username):
            return Response(data={"message": "That email already exists"}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(
            email=email,
            username=email,
            password=password
        )
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(data={"message": "Account deleted."}, status=status.HTTP_204_NO_CONTENT)






