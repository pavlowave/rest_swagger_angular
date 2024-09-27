from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Breeder, Cat

# Сериалайзер для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Хэшируем пароль
        user.save()
        return user

# Сериалайзер для заводчика
class BreederSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Вложенный сериалайзер для пользователя

    class Meta:
        model = Breeder
        fields = ['user']

# Сериалайзер для кошки
class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'fluffiness', 'breeder']
