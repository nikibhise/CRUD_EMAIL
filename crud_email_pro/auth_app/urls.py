from django.urls import path
from .views import UserAPI

urlpatterns = [
    path('users/', UserAPI.as_view()),
]
