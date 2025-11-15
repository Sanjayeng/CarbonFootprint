from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.emission_index, name='emissions_index'),
  path('add/', views.activity_add, name='activity_add'),
  
    
]
