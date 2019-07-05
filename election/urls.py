from django.urls import path
from election import views

urlpatterns = [
    path('config_mock_election/', views.config_mock_election, name='config_mock_election'),
    path('electionconfig/',views.electionConfiguration, name='electionconfig'),
    path('candidate/',views.candidate, name='candidate'),
    path('candidate/<int:id>/change', views.candidate_change, name='candidate_change'),
    path('candidate/<int:id>/delete', views.candidate_delete, name='candidate_delete'),
    path('candidate/add', views.candidate_add, name='candidate_add'),
]
