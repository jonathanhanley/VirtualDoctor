from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.db import models

from vdoc_api.models import Consultant, QuestionSet, Question, Answer

User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('user')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'code', 'password', 'is_consultant')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        pass


class ConsultantSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='user.password', write_only=True)
    email = serializers.CharField(source='user.email')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Consultant
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'code', 'password')

    def create(self, validated_data):
        return Consultant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class QuestionSetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=10000)
    first_question_id = serializers.SerializerMethodField('get_first_q_id')

    def get_first_q_id(self, question_set):
        if isinstance(question_set, QuestionSet):
            questions = Question.objects.filter(set_id=question_set.id).order_by('id')
            if questions:
                return questions[0].id
        return None

    class Meta:
        model = QuestionSet
        fields = ('id', 'consultant', 'name', 'description', 'created', 'first_question_id')

    def create(self, validated_data):
        c = validated_data.get("consultant")
        consultant = Consultant.objects.get(id=c)
        validated_data["consultant"] = consultant
        return QuestionSet.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    text = models.TextField(max_length=1028, null=True, blank=True)
    hint = models.TextField(max_length=1028, null=True, blank=True)

    class Meta:
        model = Question
        fields = ('id', 'set', 'text', 'hint', 'next_question')

    def create(self, validated_data):
        s = validated_data.get("set")
        validated_data["set"] = QuestionSet.objects.get(id=s)
        return Question.objects.create(**validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    text = models.TextField(max_length=1028, null=True, blank=True)
    question_text = serializers.SerializerMethodField('get_question_text')

    def get_question_text(self, answer):
        if isinstance(answer, Answer):
            question_text = answer.question.text
            return question_text
        return None

    class Meta:
        model = Answer
        fields = ('id', 'text', 'question_text')

    def create(self, validated_data):
        q = validated_data.get("question")
        if isinstance(q, list):
            q = int(q[0])
        validated_data["question"] = Question.objects.get(id=q)
        return Answer.objects.create(**validated_data)


