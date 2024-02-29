import cv2
import time
import numpy as np
import easyocr
from PIL import Image,ImageFont,ImageDraw
from googletrans import Translator
import cvzone
import imutils
import pygame
import requests

path = ''
play_path = 'effect/'

# 손 마우스 포인터 생성
def mouse_handler(l,x,y,ix,iy,w,h,new_img,cap_image,src):
    if x>280 : 
        if  20<l <25:
            cv2.putText(new_img,'clicked',(1100,600),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),3)
            src.append([x-(w-iy-270),y-100])
            time.sleep(0.3)
        if len(src)<3:
            for xx,yy in src:
                cv2.circle(new_img,center=(xx+(w-iy-270),yy+100),radius=5,color=(0,255,0),thickness=-1,lineType=cv2.LINE_AA)
        
    cv2.imshow('scan',new_img)
def mouse_handler12(l,x,y,ix,iy,w,h,new_img,cap_image,src2):
    if x>280 : 
        if  20<l <25:
            cv2.putText(new_img,'clicked',(1100,600),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),3)
            src2.append([x-(w-iy-270),y-100])
            pygame.init()
            pygame.mixer.init()
            sound8 = pygame.mixer.Sound( play_path+"one_click.wav" )
            sound8.play()
            time.sleep(0.3)

        for xx,yy in src2:
            cv2.circle(new_img,center=(xx+(w-iy-270),yy+100),radius=5,color=(0,255,0),thickness=-1,lineType=cv2.LINE_AA)
        
    cv2.imshow('scan',new_img)

#손 마우스 포인터 좌표 클릭
def mouse_handler2(l,x,y,ix,iy,w,h,new_img,cap_image,src):
    if len(src) == 2:
        if src[0][0] >= src[1][0] :
            src.reverse()
        src.insert(1,[src[1][0],src[0][1]])
        src.append([src[0][0],src[2][1]])
    src_np = np.array(src,dtype=np.float32)

    width = max(np.linalg.norm(src_np[0] - src_np[1]), np.linalg.norm(src_np[2]-src_np[3]))
    height = max(np.linalg.norm(src_np[0] - src_np[3]), np.linalg.norm(src_np[1]-src_np[2]))

    dst_np = np.array([[0,0],[width,0],[width,height],[0,height]],dtype = np.float32)
    M = cv2.getPerspectiveTransform(src=src_np,dst = dst_np)
    result = cv2.warpPerspective(cap_image,M,(int(width), int(height)))
    cv2.imwrite(path+'scaned.jpg',result)
    cv2.imshow('f',result)
def mouse_handler4(l,x,y,ix,iy,w,h,new_img,cap_image,src2):
    if len(src2) == 4:
        src_np = np.array(src2,dtype=np.float32)

        width = max(np.linalg.norm(src_np[0] - src_np[1]), np.linalg.norm(src_np[2]-src_np[3]))
        height = max(np.linalg.norm(src_np[0] - src_np[3]), np.linalg.norm(src_np[1]-src_np[2]))

        dst_np = np.array([[0,0],[width,0],[width,height],[0,height]],dtype = np.float32)
        M = cv2.getPerspectiveTransform(src=src_np,dst = dst_np)
        result = cv2.warpPerspective(cap_image,M,(int(width), int(height)))
        cv2.imwrite(path+'scaned.jpg',result)
        cv2.imshow('f',result)

#버튼 객체
class Button():
    def __init__(self,pos,text,size=(185,70)):  
        self.pos = pos
        self.size = size
        self.text = text
    
# buttonList안의 각원소 값으로 button그림    
# def drawAll(img,buttonList):
#     for button in buttonList:
#         x,y = button.pos
#         w,h = button.size
#         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),cv2.FILLED)
#         cv2.putText(img,button.text,(x+15,y+60),
#                 cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
#     return img
def drawAll(img,buttonList):
    imgNew = np.zeros_like(img,np.uint8)
    for button in buttonList:
        x,y = button.pos
        w,h = button.size
        cvzone.cornerRect(imgNew,(x-80,y,w,h),20,rt=0)
        cv2.rectangle(imgNew,(x-80,y),(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(imgNew,button.text,(x+15,y+60),
                cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
    out = img.copy()
    alpha = 0.3
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
    return out

# OCR

reader = easyocr.Reader(['en'],gpu=False)
reader_ko = easyocr.Reader(['ko'],gpu=False)

def OCR(new_img,sc):
    txt =''
    txt_ko =''
    txt_p = ''
    img = cv2.imread(path+'scaned.jpg')
    i=0
    while sc:
        try:
            result = reader.readtext(img)
            result_ko = reader_ko.readtext(img)
            img = Image.fromarray(img)
            font = ImageFont.truetype("./batang.ttc", 48)
            draw = ImageDraw.Draw(img)
            for i in result:
                x = i[0][0][0] 
                y = i[0][0][1] 
                w = i[0][1][0] - i[0][0][0] 
                h = i[0][2][1] - i[0][1][1]

                draw.rectangle(((x,y),(x+w,y+h)),outline=(255,255,255),width = 4)
                draw.text((x+10,y-50),i[1],font=font,fill = (0,0,255))
            
                txt += i[1]+' '

            for i in result_ko:
                txt_ko += ' '+i[1]

            cv2.putText(new_img,'ocr_complete',(500,600),cv2.FONT_HERSHEY_PLAIN,4,(0,0,255),3)

            translator = Translator()

            txt_ko = txt_ko
            
            url = 'https://openapi.naver.com/v1/papago/n2mt'
            headers = {"X-Naver-Client-Id": 'dYt0uIKrURhWVYu8vxA_', "X-Naver-Client-Secret":'Zct9JynYlA'}
            params = {"source": "en", "target": "ko", "text": txt}
            response = requests.post(url, headers=headers, data=params)
            res = response.json()
            txt_p = res['message']['result']['translatedText']

            sc = False
            er = False
        except:
            txt_p = None
            txt_ko = None
            er = True
            sc=False
            src = []
            break
    return sc,txt_p,txt_ko,er

#버튼 리스트 생성
def btlist(keys=None,keys2=None,keys3 = None):
    buttonList = []
    buttonList2 = []
    buttonList3 = []
    if keys is not None:
        for j in range(len(keys)):
            for i in range(len(keys[j])):
                buttonList.append(Button([1000*i+90,80*j+50],keys[j][i]))
    if keys3 is not None:
        for j3 in range(len(keys3)):
            buttonList3.append(Button([1090,80*j3+50],keys3[j3]))
    if keys2 is not None:
        for j2 in range(len(keys2)):
            buttonList2.append(Button([90,80*j2+50],keys2[j2]))

    return buttonList,buttonList2,buttonList3

def find_edge(img):
    try:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray,11,17,17)
        edged = cv2.Canny(bfilter,30,200)
        keypoints = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours,key=cv2.contourArea,reverse=True)[:10]

        location  = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour,10,True)
            if len(approx) ==4:
                location =approx
                break
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[location],0,255,-1)
        new_image = cv2.bitwise_and(img,img,mask=mask)
        (x,y) = np.where(mask == 255)
        (x1,y1) = (np.min(x),np.min(y))
        (x2,y2)=(np.max(x),np.max(y))
        cropped_image = gray[x1:x2+1,y1:y2+1]
        cropped_image = cv2.cvtColor(cropped_image,cv2.COLOR_GRAY2BGR)
        cropped_image = cv2.resize(cropped_image,(700,600))
        next = False
    except:
        print('error')
        next = True
    if next ==False:
        return cropped_image,img
    else :
        return img,img 