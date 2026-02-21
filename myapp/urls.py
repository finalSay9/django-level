# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
   
    path('register/', views.RegisterView.as_view(), name='register'), 
    path('login/', ... ),  # you probably already have this
]