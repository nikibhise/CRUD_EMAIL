from django.urls import path 
from .views import CrudAPI, CrudDetailsAPI

urlpatterns = [
    path('books/', CrudAPI.as_view()),
    path('books/<int:pk>/', CrudDetailsAPI.as_view()),
]