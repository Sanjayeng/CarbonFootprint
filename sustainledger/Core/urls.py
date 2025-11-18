from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'Core'
urlpatterns = [
path('', views.core_list, name='core_list'),
path('add/', views.core_add, name='core_add'),


    path('facility/', views.facility_list, name='facility_list'),
    path('facility/add/', views.facility_add, name='facility_add'),
]