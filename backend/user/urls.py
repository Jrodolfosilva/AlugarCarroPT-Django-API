from user.views.main import UserView, LoginView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('user/login/', LoginView.as_view()),
    path('user/new/', UserView.as_view()),
]
