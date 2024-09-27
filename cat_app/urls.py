from django.urls import path
from .views import BreederRegistrationView, CatCreateView

urlpatterns = [
    path('register/', BreederRegistrationView.as_view(), name='breeder-register'),
    path('add-cat/', CatCreateView.as_view(), name='cat-create'),
]