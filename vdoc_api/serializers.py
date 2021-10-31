from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.db import models

from vdoc_api.models import Consultant, QuestionSet, Question

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
        fields = ('email', 'username', 'code', 'password')

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
        fields = ('email', 'username', 'first_name', 'last_name', 'code', 'password')

    def create(self, validated_data):
        return Consultant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class QuestionSetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=10000)

    class Meta:
        model = QuestionSet
        fields = ('consultant', 'name', 'description', 'created')

    def create(self, validated_data):
        c = validated_data.get("consultant")
        consultant = Consultant.objects.get(id=c)
        validated_data["consultant"] = consultant
        return QuestionSet.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    # set = models.ForeignKey('QuestionSet', on_delete=models.CASCADE)
    text = models.TextField(max_length=1028, null=True, blank=True)
    hint = models.TextField(max_length=1028, null=True, blank=True)
    # next_question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)

    class Meta:
        model = Question
        fields = ('set', 'text', 'hint', 'next_question')



