from typing import ByteString
import easyocr
import cv2
from PIL import Image,ImageFont,ImageDraw
import matplotlib.pyplot as plt
from gtts import gTTS
from googletrans import Translator
from playsound import playsound
import re
import imutils
import requests


# translator = Translator()
translator = Translator(service_urls=[
      
      'translate.google.co.kr'
    ])

img = cv2.imread('scaned.jpg')
# img = cv2.flip(img,1)
# img = cv2.flip(img,-1)


# take korean and english in easy ocr 
reader = easyocr.Reader(['en'],gpu=False)
# read text img
result = reader.readtext(img)

# use for korean
img = Image.fromarray(img)
font = ImageFont.truetype("./batang.ttc", 48)
draw = ImageDraw.Draw(img)

# slice each other word, the 'i' have locations and word
txt = ''
for i in result:
    x = i[0][0][0] 
    y = i[0][0][1] 
    w = i[0][1][0] - i[0][0][0] 
    h = i[0][2][1] - i[0][1][1]

    draw.rectangle(((x,y),(x+w,y+h)),outline=(255,255,255),width = 4)
    draw.text((x+10,y-50),i[1],font=font,fill = (0,0,0))
    txt += ' '+i[1]
# txt2 = re.compile('[|ㄱ-ㅎ|ㅏ-ㅣ]+').sub('',txt)

print(txt)
# txt = translator.translate(txt,src = 'en',dest='ko')
url = 'https://openapi.naver.com/v1/papago/n2mt'
headers = {"X-Naver-Client-Id": 'dYt0uIKrURhWVYu8vxA_', "X-Naver-Client-Secret":'Zct9JynYlA'}
params = {"source": "en", "target": "ko", "text": txt}
response = requests.post(url, headers=headers, data=params)
res = response.json()
print(res['message']['result']['translatedText'])


plt.imshow(img)
plt.show()
# print(result)
# cv2.waitKey(0)
# # # cap.release()
# cv2.destroyAllWindows()
