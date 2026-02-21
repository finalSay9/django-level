# accounts/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
   
    path('register/', views.RegisterView.as_view(), name='register'), 
    path('login/', views.CustomLoginView.as_view(), name='login')
    
]
