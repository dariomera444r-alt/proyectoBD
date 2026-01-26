#cv/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Garage Management
    path('', views.garage, name='garage'),
    
    # Protected files
    path('protected/media/avatar/<int:perfil_id>/', views.serve_avatar, name='serve_avatar'),
    path('protected/media/<str:file_type>/<int:model_id>/<str:field_name>/', 
         views.serve_protected_file, name='serve_protected_file'),
]