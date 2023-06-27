import os.path
import os
from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.http        import JsonResponse
import json

# classification import 부분
import io
from PIL import Image
from tensorflow import keras
import warnings
warnings.filterwarnings('ignore')
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
        return render(request, 'main.html', context)

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
    pests = pest_information.objects.filter(plant_nm=species).values('pest_name', 'pest_img', 'information_no', 'plant_nm')
    print(">>>>>> debug : names = ", pests)

    length = len(pests)

    print(">>>>>> debug : queryset 길이 = ", length)
    # queryset을 json_resoponse로 담기 전 리스트에 담는다.
    # 추후 'plant_nm' -> 'pest_nm'으로 바꿔줘야 한다.
    response_json = []

    #개체 하나당 딕셔너리를 만들어줘서 리스트에 넣어준다. 리스트는 인덱스로 딕셔녀리를 가져오고. 딕셔너리(obj)는 키값으로 값을 부른다.
    for i in range(0, length):
        response_json.append({'pest_nm': pests.values()[i]['pest_name'], 'pest_img': pests.values()[i]['pest_img'], 'information_no': pests.values()[i]['information_no'], 'plant_nm': pests.values()[i]['plant_nm']})
    # response_json.append({'pest_nm': pest_nm, 'pest_img': pest_img})
    print(">>>>>>debug : pest_data = ", response_json)

    return JsonResponse(response_json, safe = False)
#병충해 정보 읽기
def viewInformation(request):
    no = request.GET['no']
    print(">>>>>> debug , no = ", no)
    no = str(no)
    if(no.isnumeric() == False):
        length = len(no)
        no = no[1:length-1]

    #pest_information 의  키 값 information_no 를 받아온다.
    information = pest_information.objects.get(information_no=no)

    print(">>>>>> debug - information : ", information)

    #ORM으로 담아온 게시글 정보를 보관
    context = {'information' : information}
    # 세션 유지
    context['name'] = request.session['session_name']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'viewInformation.html', context)


#병충해 판별 게시판
#게시판 링크
#def identification은 -> classificationApp의 def upload로 대체
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
#이미지 업로드 후 전송
def identificate(request):
    source = request.GET['src']
    print("작동")
    print(">>>>>>debug, params :", source)

    # 태성님 부분
    load_model = keras.models.load_model('model/plant_model.h5')
    load_model.summary()

    # Testing
    Li = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
          'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
          'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
          'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
          'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
          'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
          'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight',
          'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
          'Strawberry___Leaf_scorch',
          'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
          'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
          'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
          'Tomato___healthy']
    # predicting an image
    import os
    # import matplotlib.pyplot as plt
    from keras.preprocessing import image
    import numpy as np
    # 파일은 위에 source에서 불러온다
    # directory = "picture/"
    # files = [os.path.join(directory, p) for p in sorted(os.listdir(directory))]
    #

    # 이미지를 경로로 불러오기 위해 기존의 저장소에서 불러오는 방식은 주석 처리
    # image_path = source
    # 주석처리 끝

    image = Image.open(source)

    new_img = image.resize((256, 256))

    # new_img = keras.utils.load_img(image_path, target_size=(256, 256))
    img = keras.utils.img_to_array(new_img)
    img = np.expand_dims(img, axis=0)
    img = img / 255
    prediction = load_model.predict(img)
    probabilty = prediction.flatten()
    max_prob = probabilty.max()
    index = prediction.argmax(axis=-1)[0]
    class_name = Li[index]
    # ploting image with predicted class name
    # plt.figure(figsize=(4, 4))
    # plt.imshow(new_img)
    # plt.axis('off')
    # plt.title(class_name + " " + str(max_prob)[0:4] + "%")
    # plt.show()
    # Encode your PIL Image as a JPEG without writing to disk
    buffer = io.BytesIO()
    images = new_img.save(buffer, format='JPEG', quality=75)

    # You probably want
    desiredObject = buffer.getbuffer()
    context = {}
    context['class'] = class_name + " " + str(max_prob)[0:4] + "%"
    # context['imgg'] = image_path

    return render(request, 'identification_backup.html', context)

def image(request):
    # 로그인 세션 유지
    if (request.session.get('session_user_id')):

        file = request.FILES['file']

        upload_table(image=file).save()
        print(">>>>>> debug , params : ", file)

        load_model = keras.models.load_model('model/plant_model.h5')
        load_model.summary()

        # Testing
        Li = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
              'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
              'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
              'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
              'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
              'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
              'Peach___healthy',
              'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
              'Potato___Late_blight',
              'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
              'Strawberry___Leaf_scorch',
              'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
              'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
              'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
              'Tomato___healthy']
        # predicting an image
        import os
        # import matplotlib.pyplot as plt
        from keras.preprocessing import image
        import numpy as np
        directory = "media/"
        files = [os.path.join(directory, p) for p in sorted(os.listdir(directory))]
        for i in range(0, 1):
            image_path = files[i]
            new_img = keras.utils.load_img(image_path, target_size=(256, 256))
            img = keras.utils.img_to_array(new_img)
            img = np.expand_dims(img, axis=0)
            img = img / 255
            prediction = load_model.predict(img)
            probabilty = prediction.flatten()
            max_prob = probabilty.max()
            index = prediction.argmax(axis=-1)[0]
            class_name = Li[index]
            # ploting image with predicted class name
            # plt.figure(figsize=(4, 4))
            # plt.imshow(new_img)
            # plt.axis('off')
            # plt.title(class_name + " " + str(max_prob)[0:4] + "%")
            # plt.show()
            # Encode your PIL Image as a JPEG without writing to disk
            buffer = io.BytesIO()
            images = new_img.save(buffer, format='JPEG', quality=75)

            # You probably want
            desiredObject = buffer.getbuffer()
            context = {}
            context['imgg'] = image_path
            context['class'] = class_name
            context['score'] = str(max_prob * 100)[0:5] + "%"



        print(">>>>>> debug, session exists")

        context['name'] = request.session['session_name']
        context['user_id'] = request.session['session_user_id']

        return render(request, 'image.html', context)






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
    # try:
    if(pwd == pwd_con):
        user_information(user_name=name, user_id=id, user_password=pwd).save()
        messages.add_message(request, messages.INFO, "회원가입이 완료되었습니다.")
        return redirect('login')
    # elif(user_information.objects.get(user_id=id)):
    #     messages.add_message(request, messages.INFO, "이미 존재하는 ID입니다.")
    #     return redirect('join')
    else:
        messages.add_message(request, messages.INFO, "비밀번호를 확인하세요.")
        return redirect('join')

    # #입력하지 않는 정보가 있을 경우 try-except로 처리
    # except:
    #     messages.add_message(request, messages.INFO, "입력하지 않는 정보가 있습니다.")
    #     return redirect('join')

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

# 서버 내렷다 올릴때 해당 폴더안에 파일 삭제
def DeleteAllFiles(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
        return 'Remove All File'
    else:
        return 'Directory Not Found'
print(DeleteAllFiles('media/'))







