from django.urls import path
from election import views

urlpatterns = [
    path('config_mock_election/', views.config_mock_election, name='config_mock_election'),
    path('electionconfig/',views.electionConfiguration, name='electionconfig'),
]
