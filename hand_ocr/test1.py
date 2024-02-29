from locale import Error
from hand_mouse import find_edge
from cvzone.HandTrackingModule import HandDetector
from hand_mouse import *
from playsound import playsound
import cv2
import pygame
import pyttsx3

def hand_ocr(cap,cap2):
    path = ''
    play_path = "effect/"

    first_bye = False
    new_bye = False
    scan_bye = False

    
    cap.set(3,1280)
    cap.set(4,720)
    cap2.set(3,700)
    cap2.set(4,600)

    detector = HandDetector(detectionCon=0.8,maxHands=2)
    detector2 = HandDetector(detectionCon=0.8,maxHands=2)

    keys = [['close','play'],
    ['new']]

    keys3 = ['cap','scan','close']

    keys2 = ['play','p_ko','src','close']

    pic = False
    sc = False

    src = []
    src2 = []

    buttonList,buttonList2,buttonList3 = btlist(keys=keys,keys2 = keys2, keys3=keys3)


    i_window = cv2.imread(play_path+'i_window.png',cv2.IMREAD_UNCHANGED)
    i_window = cv2.resize(i_window,(70,70))
    mask_window = i_window[:,:,3]
    i_window = i_window[:,:,:-1]
    
    i_close = cv2.imread(play_path+'i_close.png',cv2.IMREAD_UNCHANGED)
    i_close = cv2.resize(i_close,(70,70))
    mask_close = i_close[:,:,3]
    i_close = i_close[:,:,:-1]

    i_play = cv2.imread(play_path+'i_play.png',cv2.IMREAD_UNCHANGED)
    i_play = cv2.resize(i_play,(70,70))
    mask_play = i_play[:,:,3]
    i_play = i_play[:,:,:-1]

    i_camera = cv2.imread(play_path+'i_camera.png',cv2.IMREAD_UNCHANGED)
    i_camera = cv2.resize(i_camera,(70,70))
    mask_camera = i_camera[:,:,3]
    i_camera = i_camera[:,:,:-1]

    i_scan = cv2.imread(play_path+'i_scan.png',cv2.IMREAD_UNCHANGED)
    i_scan = cv2.resize(i_scan,(70,70))
    mask_scan = i_scan[:,:,3]
    i_scan = i_scan[:,:,:-1]

    i_switch = cv2.imread(play_path+'i_switch.png',cv2.IMREAD_UNCHANGED)
    i_switch = cv2.resize(i_switch,(70,70))
    mask_switch = i_switch[:,:,3]
    i_switch = i_switch[:,:,:-1]

    pygame.init()
    pygame.mixer.init()
    sound1 = pygame.mixer.Sound( play_path+"open.wav" )
    sound1.play()
    while True:
        ret, img = cap.read()
        img = cv2.flip(img,1)
        if not ret:
            break

        hands = detector.findHands(img,draw = False)
        
        img = drawAll(img,buttonList)
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            # w= w+200

            if button.text == 'new':
                crop_window = img[y:y+70,x-70:x,:] 
                cv2.copyTo(i_window,mask_window,crop_window)

            if button.text == 'close':
                crop_close = img[y:y+70,x-70:x,:]
                cv2.copyTo(i_close,mask_close,crop_close) 
            
            if button.text == 'play':
                crop_play = img[y:y+70,x-70:x,:] 
                cv2.copyTo(i_play,mask_play,crop_play)

        # hand 검출되면
        if hands:
            hand = hands[0]
            lmList = hand['lmList']
            cv2.putText(img,'on',(50,600),cv2.FONT_HERSHEY_PLAIN,4,(255,0,0),3)

            cv2.circle(img,(lmList[8][0],lmList[8][1]),5,(0,0,255),-1)

            for button in buttonList:
                x,y = button.pos
                w,h = button.size
                # w= w+200

                # lmList 8:검지 끝
                # 버튼 좌표안에 검지 끝이 들어오면
                if (x-70<lmList[8][0]<x+w) and (y<lmList[8][1]<y+h) :
                    if hand['type'] in ['Left','Right']:                
                        cv2.rectangle(img,(x+10,y),(x+w,y+h),(170,0,170),cv2.FILLED)
                        cv2.putText(img,button.text,(x+15,y+60),
                                cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)

                        cv2.circle(img,(lmList[8][0],lmList[8][1]),5,(200,255,0),-1)
                        l, _ = detector.findDistance(lmList[4],lmList[12])

                        if 22<l <30:
                            cv2.rectangle(img,(x+10,y),(x+w,y+h),(0,255,0),cv2.FILLED)
                            cv2.putText(img,button.text,(x+15,y+60),
                                cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)
                            pygame.init()
                            pygame.mixer.init()
                            sound2 = pygame.mixer.Sound( play_path+"mouse_click.wav" )
                            sound2.play()
                            time.sleep(0.15)

                            if button.text =='close':
                                pygame.init()
                                pygame.mixer.init()
                                sound20 = pygame.mixer.Sound( play_path+"close.wav" )
                                sound20.play()
                                first_bye = True


                            if button.text == 'play':
                                try:
                                    translator = Translator()
                                    img = cv2.imread(path+'scaned.jpg')
                                    reader = easyocr.Reader(['en'],gpu=False)
                                    result = reader.readtext(img)
                                    txt = ''
                                    for i in result:
                                        txt += ' '+i[1]
                                    
                                    txt1 = translator.translate(txt, src='en', dest='ko')
                                    s = pyttsx3.init()
                                    s.setProperty('rate', 140)
                                    rate = s.getProperty('rate')
                                    voices = s.getProperty('voices')
                                    s.setProperty('voice', voices[0].id)
                                    s.say(txt1.text)
                                    s.runAndWait()
                                    time.sleep(0.5)
                                except :
                                    s = pyttsx3.init()
                                    s.setProperty('rate', 140)
                                    rate = s.getProperty('rate')
                                    voices = s.getProperty('voices')
                                    s.setProperty('voice', voices[0].id)
                                    s.say('스캔 부터 하시지요')
                                    s.runAndWait()

                            # 2번째 창 실행 -----------------------------------------------------------------------------------------------------------------------------------
                            if button.text == 'new':
                                pygame.init()
                                pygame.mixer.init()
                                sound150 = pygame.mixer.Sound( play_path+"close.wav" )
                                sound150.play()
                                
                                while True:
                                    ret2,img_cap = cap.read()
                                    ret3,img3 = cap2.read()
                                    if not ret2: break
                                    if not ret3: break
                                    img_cap = cv2.flip(img_cap,1)
                                    # cv2.namedWindow('cap')
                                    

                                    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                    w2 = round(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
                                    h2 = round(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

                                    # 2번째 카메라와 1번째 카메라 합성영상 만들기ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
                                    sec_cam = img_cap.copy()
                                    sec_cam[100:100+h2,w-w2-300:w-300,:] = img3
                                    # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
                                    hands = detector.findHands(img_cap,draw =False)
                                    sec_cam = drawAll(sec_cam,buttonList3)
                                    
                                    for button in buttonList3:
                                        x,y = button.pos
                                        w,h = button.size

                                        if button.text == 'cap':
                                            crop_camera = sec_cam[y:y+70,x-70:x,:]
                                            cv2.copyTo(i_camera,mask_camera,crop_camera)

                                        if button.text == 'scan':
                                            crop_scan = sec_cam[y:y+70,x-70:x,:]
                                            cv2.copyTo(i_scan,mask_scan,crop_scan)

                                        if button.text == 'close':
                                            crop_close = sec_cam[y:y+70,x-70:x,:]
                                            cv2.copyTo(i_close,mask_close,crop_close) 

                                    if pic ==True:  # capture 성공하면 텍스트 쓰기
                                        cv2.putText(sec_cam,capt,(500,500),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),3)

                                    if hands:
                                        hand = hands[0]
                                        lmList = hand['lmList']
                                        cv2.putText(sec_cam,'on',(50,600),cv2.FONT_HERSHEY_PLAIN,4,(255,0,0),3)
                                        cv2.circle(sec_cam,(lmList[8][0],lmList[8][1]),5,(0,0,255),-1)

                                        for button in buttonList3:
                                            x,y = button.pos
                                            w,h = button.size
                                    
                                            if (x-70<lmList[8][0]<x+w) and (y<lmList[8][1]<y+h) : 
                                                if hand['type'] in ['Left','Right']:               
                                                    cv2.rectangle(sec_cam,(x+10,y),(x+w,y+h),(170,0,170),cv2.FILLED)
                                                    cv2.putText(sec_cam,button.text,(x+15,y+60),
                                                            cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                                                    l, _ = detector.findDistance(lmList[4],lmList[12])

                                                    cv2.circle(sec_cam,(lmList[8][0],lmList[8][1]),5,(200,255,0),-1)

                                                    if 20<l <30:
                                                        cv2.rectangle(sec_cam,(x+10,y),(x+w,y+h),(0,255,0),cv2.FILLED)
                                                        cv2.putText(sec_cam,button.text,(x+15,y+60),
                                                            cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)
                                                        
                                                        time.sleep(0.15)
                                                        # 캡쳐  -----------------------------------------------------------------------------------------------------------------------------------
                                                        if button.text == 'cap':
                                                            cv2.imwrite(path+'cap.jpg',img3)
                                                            pygame.init()
                                                            pygame.mixer.init()
                                                            sound2 = pygame.mixer.Sound( play_path+"cam_shutter.wav" )
                                                            sound2.play()
                                                            pic = True  ## 성공 메세지 쓰기위해 True로 변환
                                                            capt = 'captured' ## 성공 메세지 내용

                                                        if button.text == 'close':
                                                            pygame.init()
                                                            pygame.mixer.init()
                                                            sound30 = pygame.mixer.Sound( play_path+"mouse_click.wav" )
                                                            sound30.play()
                                                            new_bye = True
                                                            pygame.init()
                                                            pygame.mixer.init()
                                                            sound9 = pygame.mixer.Sound( play_path+"close.wav" )
                                                            sound9.play()

                                                        # 스캔 -----------------------------------------------------------------------------------------------------------------------------------
                                                        if button.text == 'scan':
                                                            pygame.init()
                                                            pygame.mixer.init()
                                                            sound3 = pygame.mixer.Sound( play_path+"mouse_click.wav" )
                                                            sound3.play()
                                                            cap_image = cv2.imread(path+'cap.jpg')
                                                            cap_im,img = find_edge(cap_image)
                                                            edge_ch = False

                                                            pygame.init()
                                                            pygame.mixer.init()
                                                            sound240 = pygame.mixer.Sound( play_path+"close.wav" )
                                                            sound240.play()

                                                            while True:
                                                                ret2,img_t = cap.read()
                                                                if not ret2: break
                                                                cv2.namedWindow('scan', cv2.WINDOW_NORMAL)
                                                                cv2.setWindowProperty('scan', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                                                img_t = cv2.flip(img_t,1)
                                                                if edge_ch == True:
                                                                    cap_image = img
                                                                else :
                                                                    cap_image = cap_im
                                                                ix,iy,_ = cap_image.shape
                                                                w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                                                h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                                                                # 2번째 카메라와 캡쳐된 이미지 합성영상 만들기ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
                                                                new_img = img_t.copy()
                                                                new_img[100:100+ix,w-iy-270:w-270,:] = cap_image
                                                                # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
                                                                
                                                                new_img = drawAll(new_img,buttonList2)

                                                                for button in buttonList2:
                                                                    x,y = button.pos

                                                                    if button.text == 'play':
                                                                        crop_play = new_img[y:y+70,x-70:x,:]
                                                                        cv2.copyTo(i_play,mask_play,crop_play) 

                                                                    if button.text == 'p_ko':
                                                                        crop_play = new_img[y:y+70,x-70:x,:]
                                                                        cv2.copyTo(i_play,mask_play,crop_play)

                                                                    if button.text == 'src':
                                                                        crop_switch = new_img[y:y+70,x-70:x,:]
                                                                        cv2.copyTo(i_switch,mask_switch,crop_switch)

                                                                    if button.text == 'close':
                                                                        crop_close = new_img[y:y+70,x-70:x,:]
                                                                        cv2.copyTo(i_close,mask_close,crop_close)

                                                                hands = detector2.findHands(img_t,draw =False)
                                                                if hands:
                                                                    hand = hands[0]
                                                                    if hand['type'] in ['Left','Right']:
                                                                        lmList = hand['lmList']
                                                                        cv2.putText(new_img,'on',(50,600),cv2.FONT_HERSHEY_PLAIN,4,(255,0,0),3)
                                                                        cv2.circle(new_img,(lmList[8][0],lmList[8][1]),5,(0,0,255),-1)
                                                                        l, _ = detector.findDistance(lmList[4],lmList[12])

                                            ## mouse_handler 함수 호출 (l = 거리값, 엄지끝,중지끝, ix,iy = 캡쳐된 이미지 (x,y), w,h = 1번째 영상 (넓이,높이), 합성영상, 캡쳐이미지, 지정 좌표값 )
                                                                        mouse_handler(l,lmList[8][0],lmList[8][1],ix,iy,w,h,new_img,cap_image,src)
                                                                        mouse_handler12(l,lmList[8][0],lmList[8][1],ix,iy,w,h,new_img,cap_image,src2)

                                                                        if len(src) == 2:
                                                                            mouse_handler2(l,lmList[8][0],lmList[8][1],ix,iy,w,h,new_img,cap_image,src)
                                                                        if len(src2)==4:
                                                                            mouse_handler4(l,lmList[8][0],lmList[8][1],ix,iy,w,h,new_img,cap_image,src2)


                                                                        if len(src) ==4: 
                                                                            sc = True
                                                                        if len(src2) ==4: 
                                                                            sc = True

                                                                        for button in buttonList2:
                                                                            x,y = button.pos
                                                                            w,h = button.size

                                                                            if (x-70<lmList[8][0]<x+w) and (y<lmList[8][1]<y+h) : 
                                                                                if hand['type'] in ['Left','Right']:               
                                                                                    cv2.rectangle(new_img,(x+10,y),(x+w,y+h),(170,0,170),cv2.FILLED)
                                                                                    cv2.putText(new_img,button.text,(x+15,y+60),
                                                                                            cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                                                                                    l, _ = detector.findDistance(lmList[4],lmList[12])

                                                                                    cv2.circle(new_img,(lmList[8][0],lmList[8][1]),5,(200,255,0),-1)

                                                                                    if 20<l <30:
                                                                                        cv2.rectangle(new_img,(x+10,y),(x+w,y+h),(0,255,0),cv2.FILLED)
                                                                                        cv2.putText(new_img,button.text,(x+15,y+60),
                                                                                            cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)
                                                                                        
                                                                                        time.sleep(0.15)

                                                                                        if button.text == 'close':
                                                                                            pygame.init()
                                                                                            pygame.mixer.init()
                                                                                            sound60 = pygame.mixer.Sound( play_path+"mouse_click.wav" )
                                                                                            sound60.play()
                                                                                            try:
                                                                                                cv2.destroyWindow('f')
                                                                                                time.sleep(0.15)
                                                                                            except:
                                                                                                scan_bye = True
                                                                                                pygame.init()
                                                                                                pygame.mixer.init()
                                                                                                sound15 = pygame.mixer.Sound( play_path+"close.wav" )
                                                                                                sound15.play()
                                                                                                # cv2.destroyAllWindows()
                                                                                        if button.text == 'src':
                                                                                            pygame.init()
                                                                                            pygame.mixer.init()
                                                                                            sound66 = pygame.mixer.Sound( play_path+"mouse_click.wav" )
                                                                                            sound66.play()
                                                                                            edge_ch = not edge_ch
                                                                                        
                                                                                        # sound play en -----------------------------------------------------------------------------------------------------------------------------------
                                                                                        if button.text == 'play':
                                                                                            pygame.init()
                                                                                            pygame.mixer.init()
                                                                                            sound350 = pygame.mixer.Sound( play_path+"mouse_click.wav" )
                                                                                            sound350.play()
                                                                                            s = pyttsx3.init()
                                                                                            s.setProperty('rate', 140)
                                                                                            rate = s.getProperty('rate')
                                                                                            if txt == None:
                                                                                                s.say('오류 입니다. 다시 스캔 해주세요!')
                                                                                                s.runAndWait()
                                                                                                time.sleep(0.5)
                                                                                            
                                                                                            else:
                                                                                                s.say(txt)
                                                                                                s.runAndWait()
                                                                                                time.sleep(0.5)
                                                                                        # sound play ko ------------------------------------------------------------------------------------
                                                                                        if button.text == 'p_ko':
                                                                                            pygame.init()
                                                                                            pygame.mixer.init()
                                                                                            sound367 = pygame.mixer.Sound( play_path+"mouse_click.wav" )
                                                                                            sound367.play()
                                                                                            s = pyttsx3.init()
                                                                                            s.setProperty('rate', 140)
                                                                                            rate = s.getProperty('rate')
                                                                                            if txt_ko == None:
                                                                                                s.say('오류 입니다. 다시 스캔 해주세요')
                                                                                                s.runAndWait()
                                                                                                time.sleep(0.5)
                                                                                            
                                                                                            else:
                                                                                                s.say(txt_ko)
                                                                                                s.runAndWait()
                                                                                                time.sleep(0.5)
                                                                                            s.say(txt_ko)
                                                                                            s.runAndWait()
                                                                                            time.sleep(0.5)

                                                                if not hands: src=[]  ## 손이 화면 밖으로 나가면 좌표클릭 처음부터
                                                                if not hands: src2=[]  ## 손이 화면 밖으로 나가면 좌표클릭 처음부터


                                                                ## OCR ---------------------------------------------------------------------------------------------
                                                                if sc == True :
                                                                    er = False ## scan 오류시 True
                                                                    sc,txt,txt_ko,er = OCR(new_img,sc)
                                                                    print(txt)
                                                                    src =[]
                                                                    if er :
                                                                        cv2.putText(new_img,'rescan_please',(500,400),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                                                                        cv2.imshow('scan',new_img)
                                                                ##---------------------------------------------------------------------------------------------

                                                                cv2.imshow('scan',new_img)
                                                                if scan_bye == True:
                                                                    break
                                                                if cv2.waitKey(1) == 27 : break
                                                            # 스캔창 종료-------------------------------------------------------------------------------------------------------
                                                            # pygame.init()
                                                            # pygame.mixer.init()
                                                            # sound8 = pygame.mixer.Sound( play_path+"close.wav" )
                                                            # sound8.play()
                                                            cv2.destroyWindow('scan')
                                                            # -----------------------------------------------------------------------------------------------------------------------------------
                                                            capt = ' ' ## 스캔창 종료되면 capture 메세지 초기화
                                                            scan_bye = False
                                    cv2.namedWindow('cap', cv2.WINDOW_NORMAL)
                                    cv2.setWindowProperty('cap', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    cv2.imshow('cap',sec_cam)
                                    if new_bye == True:
                                        break
                                    if cv2.waitKey(1) == 27 : break
                                
                                cv2.destroyWindow('cap')
                                new_bye = False
                                # 2번째 창 종료-----------------------------------------------------------------------------------------------------------------------------------
        
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('image',img)

        if first_bye == True:
            break
        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyWindow('image')
    first_bye = False

    return first_bye






cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

hand_ocr(cap,cap2)