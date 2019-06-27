from django.contrib import admin
from django.urls import path
from election import views

urlpatterns = [
    path('vote', views.vote, name='vote'),
]
