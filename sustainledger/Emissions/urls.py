from django.urls import path
from . import views

urlpatterns = [
    path('', views.emission_index, name='emission_index'),
    path('add/', views.activity_add, name='activity_add'),
]
