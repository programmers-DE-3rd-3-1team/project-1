from django.urls import path, include
from . import views

app_name = 'boots'

urlpatterns = [
    path('index/', views.index),
]