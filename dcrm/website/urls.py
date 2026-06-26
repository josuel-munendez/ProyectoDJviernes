from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registrar/', views.register_user, name='register'),
    path('record/<str:pk>/', views.customer_record, name='customer_record'),
    path('delete_record/<str:pk>/', views.delete_record, name='delete_record'),
    path('update_record/<str:pk>/', views.update_record, name='update_record'),
    path('buscar/', views.search_records, name='search'),
]

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'
