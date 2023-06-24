from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.http        import JsonResponse
import json


# Create your views here.


#로그인 후 메인화면
def main(request):
    print(">>>>>>debug client path: / main() , render main.html")

    #로그인 세션 유지
    if(request.session.get('session_user_id')):
        print(">>>>>> debug, session exists")
        context = {}
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']
        return render(request, 'main2.html', context)

    return render(request, 'main.html')

#게시판 링크
#병충해 정보 게시판
#게시판 링크
def information(request):
    print(">>>>>>debug client path: information/ information(), render information.html")
    # 로그인 세션 유지
    if (request.session.get('session_user_id')):
        print(">>>>>> debug, session exists")

        # 게시판 정보 전달
        # all() - 전체 데이터 검색
        pests = pest_information.objects.all()

        # patinator 작업(pagninator에 데이터를 담아 갯수만큼 출력 나머지는 페이지를 넘김)
        page = int(request.GET.get('page', 1))
        paginator = Paginator(pests, 20)
        pest_list = paginator.get_page(page)

        # 추후 paginator 작업 필요
        # 지금은 orm으로 불러온것만
        context = {'pests': pest_list}

        # context = {}
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']
        return render(request, 'information.html', context)


    messages.add_message(request, messages.INFO, "로그인이 필요합니다.")
    return render(request, 'login.html')
#select box dom 통신 1.카테고리 선택
def category(request):
    print(">>>>>> debug, client path: category/ category(), render JsonResponse")

    # ajax data: 의 값 항목에서 받아오는 것임 / html id 선택자로 받아오는 것이 아니다.
    category = request.POST['plant_category']
    print(">>>>>> param = ", category)

    #불러온 카테고리에 해당한 값을 pest_information db에서 불러옴
    names = pest_information.objects.filter(plant_category=category).values('plant_nm')
    print(">>>>>> debug : names = ", names)


    species = []

    # plant_category QuerySet의 길이
    length = len(names)

    print(">>>>>>debug : queryset 길이 = ", length)

    #queryset을 json_resoponse로 담기 전 리스트에 담는다.
    for i in range(0, length) :
        species.append(names.values()[i]['plant_nm'])

    # 중복된 값을 처리하고 다시 리스트로 변화
    species = set(species)
    species = list(species)
    species = sorted(species)
    species.insert(0, '작물명')

    print(">>>>>> debug: species = ", species)

    # species라는 변수로 plant_category와 일치하는 plant_nm 을 보내준다.

    response_json = []
    response_json.append({'category': category, 'species': species})

    print(">>>>>> debug : response_json = ", response_json)

    return JsonResponse(response_json, safe = False)
#selectbox dom 통신 2. 작물명 선택
def species(request):
    print(">>>>>> debug, client path: species/ species(), render JsonResponse")

    # ajax data: 의 값 항목에서 받아오는 것임 / html id 선택자로 받아오는 것이 아니다.
    species = request.POST['plant_species']
    print(">>>>>> param = ", species)

    # 불러온 카테고리에 해당한 값을 pest_information db에서 불러옴
    # 우선 지금 db가 안바뀌어서 values 그대로 사용 추후 values('pest_nm')으로 바꿔줘야 한다.
    pests = pest_information.objects.filter(plant_nm=species).values('pest_name', 'pest_img', 'information_no')
    print(">>>>>> debug : names = ", pests)

    length = len(pests)

    print(">>>>>> debug : queryset 길이 = ", length)
    # queryset을 json_resoponse로 담기 전 리스트에 담는다.
    # 추후 'plant_nm' -> 'pest_nm'으로 바꿔줘야 한다.
    response_json = []

    #개체 하나당 딕셔너리를 만들어줘서 리스트에 넣어준다. 리스트는 인덱스로 딕셔녀리를 가져오고. 딕셔너리(obj)는 키값으로 값을 부른다.
    for i in range(0, length):
        response_json.append({'pest_nm': pests.values()[i]['pest_name'], 'pest_img': pests.values()[i]['pest_img'], 'information_no': pests.values()[i]['information_no']})
    # response_json.append({'pest_nm': pest_nm, 'pest_img': pest_img})
    print(">>>>>>debug : pest_data = ", response_json)

    return JsonResponse(response_json, safe = False)
#병충해 판별 링크
def viewInformation(request):
    no = request.GET['no']
    length = len(no)
    information_no = no[1:length-1]

    #pest_information 의  키 값 information_no 를 받아온다.
    print(">>>>>> debug , params = ", information_no)

    information = pest_information.objects.get(information_no=information_no)

    print(">>>>>> debug - information : ", information)

    #ORM으로 담아온 게시글 정보를 보관
    context = {'information' : information}
    # 세션 유지
    context['name'] = request.session['session_name']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'viewInformation.html', context)

def identification(request):
    print(">>>>>>debug client path: identification/ identification(), render identification.html")

    # 로그인 세션 유지
    if (request.session.get('session_user_id')):

        print(">>>>>> debug, session exists")
        context = {}
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']
        return render(request, 'identification.html', context)

    messages.add_message(request, messages.INFO, "로그인이 필요합니다.")
    return render(request, 'login.html')

#정보 공유 게시판
def communicate(request):
    print(">>>>>>debug client path: communicate/ communicate(), render communicate.html")

    # 로그인 세션 유지
    if (request.session.get('session_user_id')):
        print(">>>>>> debug, session exists")
        # 게시판 정보 전달
        #all() - 전체 데이터 검색

        boards = board_information.objects.all().order_by('-board_no')

        #patinator 작업(pagninator에 데이터를 담아 갯수만큼 출력 나머지는 페이지를 넘김)
        page = int(request.GET.get('page', 1))
        paginator = Paginator(boards, 15)
        board_list = paginator.get_page(page)

        context = {'boards': board_list}

        #로그인 세션
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']

        return render(request, 'communicate.html', context)

    messages.add_message(request, messages.INFO, "로그인이 필요합니다.")
    return render(request, 'login.html')


#회원 기능
#로그인 폼
def login(request):
    # !!!!!!!! 나중에 구현할 것
    # 추후 로그인 시 홈으로 보내는 기능 구현 필요(기타 사이트도 마찬가지이다)
    print(">>>>>>debug client path: login/ login(), render login.html")

    return render(request, 'login.html')

#가입 폼
def join(request):
    print(">>>>>>debug client path: join/ join(), render join.html ")

    return render(request, 'join.html')

#가입 : 정보 db등록
def register(request):
    name    = request.POST['name']
    id      = request.POST['id']
    pwd     = request.POST['pwd']
    pwd_con = request.POST['pwd_con']

    print(">>>>>>debug, params : ", name, id, pwd, pwd_con)
    #비밀번호(pwd)와 비밀번호 확인(pwd_con)이 일치해야 회원가입이 진행됨
    #그렇지 않은 경우 다시 회원가입 사이트로 돌아간 뒤
    try:
        if(pwd == pwd_con):
            if(user_information.objects.get(user_id=id)):
                messages.add_message(request, messages.INFO, "이미 존재하는 ID입니다.")
                return redirect('join')
            else:
                user_information(user_name = name, user_id = id, user_password = pwd).save()
                messages.add_message(request, messages.INFO, "회원가입이 완료되었습니다.")
                return redirect('login')
        else:
            messages.add_message(request, messages.INFO, "비밀번호를 확인하세요.")
            return redirect('join')
    #입력하지 않는 정보가 있을 경우 try-except로 처리
    except user_information.DoesNotExist:
        user = None
        messages.add_message(request, messages.INFO, "입력하지 않는 정보가 있습니다.")
        return redirect('join')

#로그인
def check(request):
    id  = request.POST['id']
    pwd = request.POST['pwd']
    print('>>>>> debug, params ', id, pwd)

    #id, pwd가 틀렸을 경우 방지하기 위해서 try-except
    try:
        user = user_information.objects.get(user_id =id, user_password = pwd)
    except user_information.DoesNotExist:
        user = None
    print(">>>>> debug, result = ", user)

    if(user):
        # 데이터를 심는 작업  - 콘텍스트 심어줘서 동적인 작업 해주는 것임
        # dict 형식으로
        # 세션 생성
        request.session['session_name'] = user.user_name
        request.session['session_user_id'] = user.user_id
        context = {}
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']
        return render(request, 'main2.html', context)

    elif(user == None):
        messages.add_message(request, messages.INFO, "없는 회원 정보 입니다.")
        return redirect('login')

def logout(request):
    print(">>>>>> debug, client path : logout / logout() call, reditrect home")
    request.session['session_name'] = {}
    request.session['session_user_id'] = {}
    return redirect('home')






