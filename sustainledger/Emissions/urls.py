from django.urls import path
from . import views

urlpatterns = [
    path('', views.emission_index, name='emission_index'),
    path('add/', views.activity_add, name='activity_add'),
     path('edit/<int:pk>/', views.activity_edit, name='activity_edit'),
    path('delete/<int:pk>/', views.activity_delete, name='activity_delete'),
]
