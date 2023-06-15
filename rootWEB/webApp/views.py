from django.shortcuts import render


# Create your views here.


#로그인 후 메인화면
def main(request):
    print(">>>>>>debug client path: / main() , render main.html")

    return render(request, 'main.html')

#게시판 링크
#병충해 정보 링크
def information(request):
    print(">>>>>>debug client path: information/ information(), render information.html")

    return render(request, 'information.html')

#병충해 판별 링크
def identification(request):
    print(">>>>>>debug client path: identification/ identification(), render identification.html")

    return render(request, 'identification.html')

#회원가입
def join(request):
    print(">>>>>>debug client path: join/ join(), render join.html ")

    return render(request, 'join.html')
