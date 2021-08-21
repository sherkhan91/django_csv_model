from django.urls import path
from .import views

urlpatterns = [
    path('',views.index, name='index'),
    path('getinformation', views.getinformation, name='getinformation'),
    path('getinformationbyid/<int:pk>', views.getinformationbyid, name='getinformationbyid'),
    path('readinformation', views.readinformation, name='readinformation'),
]