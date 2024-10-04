from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create_user/', views.create_user, name='create_user'),
    path('admin/update_user/<int:pk>/', views.update_user, name='update_user'),
    path('admin/delete_user/<int:pk>/', views.delete_user, name='delete_user'),
]
