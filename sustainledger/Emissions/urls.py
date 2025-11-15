from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path ('core/admin/', admin.site.urls),

    path('core/', include('Core.urls')),

    path('emissions/', views.emission_index, name='emissions_index'),
    path('emissions/add/', views.activity_add, name='activity_add'),
]
