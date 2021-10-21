from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('subir/', views.cargar_csv, name='cargar'),
    path('mapas/',views.maps_app,name="tablasV1"),
 
] 