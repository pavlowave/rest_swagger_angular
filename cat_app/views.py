from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import Breeder, Cat
from .serializers import BreederSerializer, CatSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class RegisterBreederView(generics.CreateAPIView):
    queryset = Breeder.objects.all()
    serializer_class = BreederSerializer  # Сериализатор для Breeder

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()  # Сохраняем пользователя
            breeder = Breeder.objects.create(user=user, name=request.data['name'], email=request.data['email'])
            token, created = Token.objects.get_or_create(user=user)  # Создаем токен для пользователя
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Список котов и создание нового кота
class CatListCreateView(generics.ListCreateAPIView):
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только котов текущего заводчика
        return Cat.objects.filter(breeder__user=self.request.user)

    def perform_create(self, serializer):
        # Проверяем, есть ли у пользователя объект Breeder
        try:
            breeder = Breeder.objects.get(user=self.request.user)
        except Breeder.DoesNotExist:
            raise ValidationError("Текущий пользователь не является заводчиком.")
        serializer.save(breeder=breeder)


# Детали кота (получение, обновление и удаление только для своего кота)
class CatDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только котов текущего заводчика
        breeder = Breeder.objects.filter(user=self.request.user).first()
        if breeder:
            return Cat.objects.filter(breeder=breeder)
        return Cat.objects.none()