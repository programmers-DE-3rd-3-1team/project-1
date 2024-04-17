from django.urls import include, path
from . import views

urlpatterns = [
    path('api/data/', views.get_data, name='api-data'),
    path('index/', views.index),
]