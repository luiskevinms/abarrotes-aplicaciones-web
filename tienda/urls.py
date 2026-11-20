from django.urls import path
from . import views

urlpatterns = [
    path("productos/", views.productos),                   
    path("productos/<int:id>/", views.producto),          
    path("productos/codigo/<str:codigo>/", views.producto_por_codigo),  

    path("ventas/", views.ventas),                         
    path("ventas/<int:id>/", views.venta),                 
]
