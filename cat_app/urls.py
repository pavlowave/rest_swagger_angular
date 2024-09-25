from django.urls import path
from .views import CatListCreateView, CatDetailView, RegisterBreederView

urlpatterns = [
    path('register_breeder/', RegisterBreederView.as_view(), name='register_breeder'),
    path('cats/', CatListCreateView.as_view(), name='cat_list_create'),
    path('cats/<int:pk>/', CatDetailView.as_view(), name='cat_detail'),
]