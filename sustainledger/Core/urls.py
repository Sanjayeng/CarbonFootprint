from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'Core'
urlpatterns = [
path('', views.index, name='index'),
path('add/', views.add_core, name='add_core'),
]