from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Breeder, Cat
from .serializers import BreederSerializer, UserSerializer, CatSerializer


class BreederRegistrationView(generics.CreateAPIView):
    queryset = Breeder.objects.all()
    serializer_class = BreederSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user')  # Извлекаем данные для пользователя
        if user_data is None:
            return Response({"error": "User data is required."}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()  # Создаем пользователя
            breeder = Breeder.objects.create(user=user)  # Создаем объект Breeder, связывая с пользователем

            # Сериализуем и возвращаем данные
            breeder_serializer = self.get_serializer(breeder)
            return Response(breeder_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CatCreateView(generics.CreateAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        breeder = Breeder.objects.get(user=self.request.user)  # Получаем заводчика по текущему пользователю
        serializer.save(breeder=breeder)  # Привязываем кота к заводчику
