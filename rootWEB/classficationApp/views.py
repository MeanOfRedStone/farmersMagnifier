from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import io
from PIL import Image

from django.contrib import messages
import os                       # for working with files
import numpy as np              # for numerical computationss
import pandas as pd             # for working with dataframes
import torch                    # Pytorch module
import matplotlib.pyplot as plt # for plotting informations on graph and images using tensors
import torch.nn as nn           # for creating  neural networks
from torch.utils.data import DataLoader # for dataloaders
from PIL import Image           # for checking images
import torch.nn.functional as F # for functions for calculating loss
import torchvision.transforms as transforms   # for transforming images into tensors
from torchvision.utils import make_grid       # for data checking
from torchvision.datasets import ImageFolder  # for working with classes and images
from torchsummary import summary              # for getting the summary of our model
import tensorflow as ts
from tensorflow import keras
import itertools
#from sklearn.metrics import precision_score, accuracy_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
import warnings
warnings.filterwarnings('ignore')
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from sklearn.preprocessing import label_binarize
# from sklearn.metrics import precision_recall_curve
#
#  # %matplotlib inline
# from tensorflow.keras.models import load_model


# %matplotlib inline
# Create your views here.
def upload(request):
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
def classfication(request):
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
    directory = "picture/"
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
        context['class'] = class_name + " " + str(max_prob)[0:4] + "%"
        context['imgg'] = image_path


    return render(request, 'identification.html',context)

