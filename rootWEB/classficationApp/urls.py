from django.urls import path
from classficationApp import views

urlpatterns = [

    path('upload/', views.upload, name ="upload"),
    path('classfication/', views.classfication, name ="classfication"),

]