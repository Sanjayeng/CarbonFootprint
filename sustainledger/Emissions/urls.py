from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('emissions/', views.EmissionList.as_view(), name='emission-list'),
]
