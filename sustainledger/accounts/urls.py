from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
path('register/', views.register_view, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('dashboard/', views.dashboard_view , name='dashboard'),
path('profile/', views.profile_view , name='profile'),
path('profile/update/', views.profile_update, name='profile_update'),
    path('dashboard/data/', views.dashboard_data_api, name='dashboard_data_api'),
    path('profile/', views.profile_view, name='profile'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/read/<int:pk>/', views.mark_notification_read, name='notif_read'),
    path('activity/', views.activity_log, name='activity'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
