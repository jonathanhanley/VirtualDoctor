from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from vdoc_api.custom_permissions import UserPermissions, ConsultantPermissions, QuestionSetPermissions, \
    AnswerPermissions
from vdoc_api.models import Consultant, QuestionSet, Question, Answer
from vdoc_api.serializers import UserSerializer, ConsultantSerializer, QuestionSetSerializer, QuestionSerializer, \
    AnswerSerializer

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
        data = request.query_params
        is_consultant = Consultant.objects.filter(user=request.user)
        if is_consultant:
            consultant = is_consultant.last()
        else:
            consultant = False
        if not data.get("id") and consultant:
            users = User.objects.filter(code=consultant.code)
            serializer = UserSerializer(users, many=True)
        elif data.get("id") and consultant:
            user = User.objects.filter(code=consultant.code, id=data.get("id"))
            if user:
                user = user.last()
                serializer = UserSerializer(user)
            else:
                return Response({}, status.HTTP_404_NOT_FOUND)
        else:
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
        elif Consultant.objects.filter(user=request.user) and data.get("user_id"):
            consultant = Consultant.objects.get(user=request.user)
            u_id = data.get("user_id")
            user = User.objects.filter(id=u_id, code=consultant.code)
            if user:
                user = user.last()
                questions_answered = Answer.objects.filter(user=user)
                questions_sets = set()
                for answer in questions_answered:
                    questions_sets.add(answer.question.set)
                serializer = QuestionSetSerializer(questions_sets, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
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
        q = serializer.create(request.data)
        data = dict(serializer.data)
        data["id"] = q.id
        return Response(data, status=status.HTTP_201_CREATED)


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

    def post(self, request):
        data = request.data
        set = data.get("set")
        text = data.get("text")
        hint = data.get("hint")
        if not set:
            return Response({"message": "Set is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not text:
             return Response({"message": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not hint:
            return Response({"message": "Hint is required"}, status=status.HTTP_400_BAD_REQUEST)

        prev_q = False
        if request.data.get("prev_question"):
            prev_q = request.data.get("prev_question")
            request.data.pop("prev_question")
        serializer = QuestionSerializer(request.data)
        q = serializer.create(request.data)
        data = dict(serializer.data)
        data["id"] = q.id
        response = Response(data, status=status.HTTP_201_CREATED)
        if prev_q:
            pq = Question.objects.get(id=prev_q)
            pq.next_question = q
            pq.save()
        return response


class APIAnswer(APIView):
    permission_classes = [AnswerPermissions]

    def post(self, request):
        question = request.data.get("question")
        text = request.data.get("text")
        if not question:
            return Response({"message": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not text:
            return Response({"message": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

        data = dict(request.data)
        data["text"] = data["text"][0]
        data["user"] = request.user
        serializer = AnswerSerializer(data)
        ans = serializer.create(data)
        ans = ans.get_next_question()
        if ans:
            ans_id = ans.id
        else:
            ans_id = None
        data = {"next_q": ans_id, "next_q_text": str(ans)}
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request):
        data = request.query_params
        if Consultant.objects.filter(user=request.user):
            consultant = Consultant.objects.get(user=request.user)
            user_id = data.get("user_id")
            set_id = data.get("set_id")
            question_set = QuestionSet.objects.filter(id=set_id, consultant=consultant)
            user = User.objects.filter(id=user_id, code=consultant.code)
            if question_set and user:
                question_set = question_set.last()
                user = user.last()
                answers = Answer.objects.filter(question__set=question_set, user=user).order_by("id")
                serializer = AnswerSerializer(answers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        return Response({}, status.HTTP_404_NOT_FOUND)


