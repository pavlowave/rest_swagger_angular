from rest_framework import serializers
from .models import Breeder, Cat
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']  # Добавьте другие поля, если необходимо
        extra_kwargs = {'password': {'write_only': True}}  # Указываем, что пароль только для записи

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Хэшируем пароль
        user.save()
        return user

class BreederSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breeder
        fields = ['name', 'email']  # Поля для создания заводчика


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['id', 'name', 'age', 'breed', 'fluffiness', 'breeder']