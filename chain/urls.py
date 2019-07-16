from django.contrib import admin
from django.urls import path
from chain import views
from django.urls import include


urlpatterns = [
    path('block_list', views.block_list, name='block_list'),
    path('block_add', views.block_add, name='block_add'),
    path('source_code_hash/<int:bblock_id>', views.source_code_hash, name='source_code_hash'),
    path('database_hash/<int:bblock_id>', views.database_hash, name='database_hash'),
]
