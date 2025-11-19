from django.urls import path
from . import views

app_name = "emissions" 

urlpatterns = [
    # Home page listing all emissions
    path('', views.emission_index, name='emission_home'),

    # View emissions for a specific facility
    path("<int:facility_id>/", views.emission_index, name="emission_index"),

    # Add / Edit / Delete
    path('add/', views.activity_add, name='activity_add'),
    path('edit/<int:pk>/', views.activity_edit, name='activity_edit'),
    path('delete/<int:pk>/', views.activity_delete, name='activity_delete'),

    # Graph + PDF report
    path('graph/', views.emission_graph, name='emission_graph'),
    path('report/pdf/', views.emission_report_pdf, name='emission_report_pdf'),
]
