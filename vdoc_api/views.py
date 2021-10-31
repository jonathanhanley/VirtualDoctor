from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from vdoc_api.custom_permissions import UserPermissions, ConsultantPermissions, QuestionSetPermissions
from vdoc_api.models import Consultant, QuestionSet, Question
from vdoc_api.serializers import UserSerializer, ConsultantSerializer, QuestionSetSerializer, QuestionSerializer

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
        code = request.data.get("code")
        username = email
        if not email:
            return Response(data={"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response(data={"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response(data={"message": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username) or User.objects.filter(username=username):
            return Response(data={"message": "That email already exists"}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(
            email=email,
            username=email,
            password=password,
            code=code,
        )
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(data={"message": "Account deleted."}, status=status.HTTP_204_NO_CONTENT)


class APIConsultant(APIView):
    permission_classes = [ConsultantPermissions]

    def get(self, request):
        consultant = Consultant.objects.get(user=request.user)
        serializer = ConsultantSerializer(consultant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = email
        if not email:
            return Response(data={"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response(data={"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not first_name:
            return Response(data={"message": "First Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not last_name:
            return Response(data={"message": "Last Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username) or User.objects.filter(username=username):
            return Response(data={"message": "That email already exists"}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(
            email=email,
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        consultant = Consultant.objects.create(
            user=user,
        )
        consultant.save()
        serializer = ConsultantSerializer(consultant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(data={"message": "Account deleted."}, status=status.HTTP_204_NO_CONTENT)


class APIQuestionSet(APIView):
    permission_classes = [QuestionSetPermissions]

    def get(self, request):
        data = request.query_params
        if data.get("id"):
            question_set = QuestionSet.objects.filter(id=data.get("id"))
            if len(question_set) > 0:
                serializer = QuestionSetSerializer(question_set[0])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "No question set was found matching that ID"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        data["consultant"] = Consultant.objects.get(user=request.user).id
        name = data.get("name")
        description = data.get("description")
        if not name:
            return Response({"message": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not description:
             return Response({"message": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = QuestionSetSerializer(request.data)
        serializer.create(request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class APIQuestion(APIView):
    permission_classes = [QuestionSetPermissions]

    def get(self, request):
        data = request.query_params
        if data.get("id"):
            question_set = Question.objects.filter(id=data.get("id"))
            if len(question_set) > 0:
                serializer = QuestionSerializer(question_set[0])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "No question set was found matching that ID"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)



