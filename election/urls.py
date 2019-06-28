from django.contrib import admin
from django.urls import path
from election import views

urlpatterns = [
    path('vote', views.vote, name='vote'),
    path('config_mock_election/', views.config_mock_election, name='config_mock_election'),
]
