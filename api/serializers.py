
from rest_framework import serializers
from .models import User, WatchedAnime
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'preferences')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class WatchedAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedAnime
        fields = '__all__'
