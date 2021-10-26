from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from vdoc_api.models import Consultant

User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('user')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

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


