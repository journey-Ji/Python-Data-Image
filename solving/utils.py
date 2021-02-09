import cv2
import numpy as np

BLUE=0
GREEN=1
RED=2

#특정한 색상의 모든 단어가 포함된 이미지를 추출합니다.
def get_chars(image,color):
    other_1=(color+1)%3
    other_2=(color+2)%3
#불러온 색상값을 파란색이라고 했을 때,
    c=image[:,:,other_1]==255 #초록색 영역을 선택
    image[c]=[0,0,0] #검은색으로 !
    c = image[:, :, other_2] == 255 # 빨간색 영역을 선택
    image[c] = [0, 0, 0] # 검은색으로 !
    c = image[:,:,color] <170 # 나머지 부분(섞인부분)도 !
    image[c] = [0, 0, 0] # 검은색으로 !
    c = image[:,:,color] != 0 # 파란색인부분을 선택
    image[c] = [255, 255, 255] # 하얀색으로 !
    return image

def extract_chars(image):
    chars=[]
    colors=[BLUE,GREEN,RED]
    for color in colors:
        image_from_one_color=get_chars(image.copy(),color) #이미지를 색상별로 추출
        image_gray=cv2.cvtColor(image_from_one_color,cv2.COLOR_BGR2GRAY)#추출된 이미지를 gray색상으로 변경
        ret,thresh=cv2.threshold(image_gray,127,255,0)#컨투어링을 위해 흑백으로 나
        #RETR_EXTERNAL 옵션으로 숫자의 외각을 기준으로 분리
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            #추출된 이미지 크기가 50이상인 경우만 실제 문잦 데이터인 것으로 파악
            #쓰레기값들을 삭제해주기 위
            area = cv2.contourArea(contour)
            if area>50:
                x,y,width,height=cv2.boundingRect(contour)
                roi=image_gray[y:y+height,x:x+width]
                chars.append((x, roi))
                #추출한 이미지를 x축을 기준으 순서대로 정렬을 해준다.
                chars=sorted(chars, key=lambda char:char[0])
    return chars
#추출한 이미지를 모두 동일한 크기인 20*20으로 바꿔줌
def resize20(image):
    resized=cv2.resize(image,(20,20))
    return resized.reshape(-1,400).astype(np.float32)
