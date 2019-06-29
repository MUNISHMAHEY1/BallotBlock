from django.urls import path
from vote import views

urlpatterns = [
    path('vote', views.vote, name='vote'),
]

