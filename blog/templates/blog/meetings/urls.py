from django.urls import path
from . import views

urlpatterns = [
    path('dodaj/', views.home, name='blog-home'),



]