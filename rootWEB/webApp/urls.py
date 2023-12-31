from django.urls import path
from webApp import views

urlpatterns = [

    #로그인 후 메인화면
    path('home/', views.main, name='home'),

    #게시판 링크
    #병충해 정보 게시판
    #게시판 링크
    path('information/', views.information),
    #selectbox dom 통신 1. 카테고리 선택
    path('category/', views.category),
    #selectbox dom 통신 2. 작물명 선택
    path('species/', views.species),
    #정보게시판 글 읽기
    path('viewInformation/', views.viewInformation),


    # 병충해 판별 게시판
    # 게시판 링크 -> classificationApp의 url upload 에서 대체한다.
    path('identification/', views.identification),
    # path('upload/', views.upload, name ="upload"),
    # 이미지 업로드 후 전송
    path('identificate/', views.identificate),
    #이미지 업로드 후 저장
    path('image/', views.image),
    # #이미지 파일 삭제
    # path('DeleteAllFiles/', views.DeleteAllFiles),



    #정보 공유 게시판
    path('communicate/', views.communicate),

    #회원 기능
    #로그인 폼
    path('login/', views.login, name='login'),
    #가입 폼
    path('join/', views.join, name='join'),
    #등록
    path('register/', views.register),
    #로그인
    path('check/', views.check),
    #로그아웃
    path('logout/', views.logout),

]