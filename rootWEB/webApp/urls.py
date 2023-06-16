from django.urls import path
from webApp import views

urlpatterns = [

    #로그인 후 메인화면
    path('home/', views.main),

    #게시판 링크
    #병충해 정보
    path('information/', views.information),
    #병충해 판별
    path('identification/', views.identification),

    #회원 기능
    #로그인
    path('login/', views.login),
    #가입 폼
    path('join/', views.join),
    #등록
    path('register/', views.register),

]