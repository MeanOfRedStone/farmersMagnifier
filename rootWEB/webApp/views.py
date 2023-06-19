from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages


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
#병충해 정보 링크
def information(request):
    print(">>>>>>debug client path: information/ information(), render information.html")
    # 로그인 세션 유지
    if (request.session.get('session_user_id')):
        print(">>>>>> debug, session exists")
        context = {}
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']
        return render(request, 'information.html', context)

    return render(request, 'information.html')

#병충해 판별 링크
def identification(request):
    print(">>>>>>debug client path: identification/ identification(), render identification.html")

    # 로그인 세션 유지
    if (request.session.get('session_user_id')):
        print(">>>>>> debug, session exists")
        context = {}
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']
        return render(request, 'identification.html', context)

    return render(request, 'identification.html')

#정보 공유 게시판
def communicate(request):
    print(">>>>>>debug client path: communicate/ communicate(), render communicate.html")

    # 로그인 세션 유지
    if (request.session.get('session_user_id')):
        print(">>>>>> debug, session exists")
        context = {}
        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']
        return render(request, 'communicate.html', context)

    return render(request, 'communicate.html')


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






