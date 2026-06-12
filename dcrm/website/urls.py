from django.urls import path
from . import views  # Importa el archivo views.py de la misma carpeta

urlpatterns = [  # type: ignore
    path('', views.home, name='home'), # Aquí SÍ va el path # type: ignore
    path('login/', views.login_user, name='login'), # type: ignore
    path('logout/', views.logout_user, name='logout'), # type: ignore
    path('registrar/',views.register_user, name='register'),
    
]