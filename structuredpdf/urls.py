from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('uploadfile/',views.fileUpload,name='uploadfile'),
    path('digi-list/',views.digitizedList,name='digi-list')
]
