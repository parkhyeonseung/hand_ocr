from keras.models import load_model
from PIL import Image, ImageOps
import cv2
import numpy as np
import test1
import time
import datetime
import pygame
import pyttsx3

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

cap.set(3,1280)
cap.set(4,720)

access = ''

path = ''
path1 = 'permission_people/'
play_path = 'effect/'

all_bye = False

i_person = cv2.imread(play_path+'i_person.png',cv2.IMREAD_UNCHANGED)
i_person = cv2.resize(i_person,(600,600))
x,y,_ = i_person.shape
mask_person = i_person[:,:,3]
i_person = i_person[:,:,:-1]

while True:
    ret, frame_f = cap.read()
    if not ret: break
    frame_f = cv2.flip(frame_f,1)
    frame = frame_f.copy()
    crop_person = frame_f[100:100+x,300:300+y,:]
    cv2.copyTo(i_person,mask_person,crop_person)
    size = (224, 224)
    image = cv2.resize(frame, size)
    image = Image.fromarray(image)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

    image = np.array(image)

    max_prediction = max(prediction[0])

    if access == True:
        cv2.putText(frame_f,'login acess',(600,600),
                cv2.FONT_HERSHEY_PLAIN,5,(0,255,0),5)

        datetime_object = datetime.datetime.now()
        date_time = datetime_object.strftime("%m_%d_%Y__%H_hor_%M_min_%S_sec")

        cv2.imwrite(path1+f'_{date_time}.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        s = pyttsx3.init()
        s.setProperty('rate', 150)
        rate = s.getProperty('rate')
        voices = s.getProperty('voices')
        s.setProperty('voice', voices[0].id)
        s.say('환영합니다 '+name+'님')
        s.runAndWait()

        all_bye = test1.hand_ocr(cap,cap2)
        pygame.init()
        pygame.mixer.init()
        sound4 = pygame.mixer.Sound(play_path+"close.wav" )
        sound4.play()

    elif access == False:
        cv2.putText(frame_f,'who are you?',(600,600),
                cv2.FONT_HERSHEY_PLAIN,5,(0,0,255),5)

    if prediction[0][1] > 0.25:
        access = True
        name = '박현승'
    elif prediction[0][2] > 0.25:
        access = True
        name = '이준혁'   

    else :
        access = False
    
    if access == True:
        cv2.putText(frame_f,'login access',(600,400),
                cv2.FONT_HERSHEY_PLAIN,5,(0,255,0),5)
        time.sleep(0.1)

    cv2.imshow('img', frame_f)
    # cv2.imshow('img2', image)

    if cv2.waitKey(1) == 27: break
    if all_bye == True : break
cap.release()
cap2.release()
cv2.destroyAllWindows()
