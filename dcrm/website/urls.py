from django.urls import path
from . import views
from .export import export_csv

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registrar/', views.register_user, name='register'),
    path('record/<str:pk>/', views.customer_record, name='customer_record'),
    path('delete_record/<str:pk>/', views.delete_record, name='delete_record'),
    path('update_record/<str:pk>/', views.update_record, name='update_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('buscar/', views.search_records, name='search'),
    path('users/', views.user_list, name='user_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('exportar-csv/', export_csv, name='export_csv'),
]

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'
