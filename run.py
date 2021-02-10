import numpy as np
import cv2
import utils
import requests #특정웹사이트와 통신하기 위한 라이브러리
import shutil
import time

FILE_NAME = "trained.npz"

#각 글자의 (1*400) 데이터와 정답(0~9, + , *)
with np.load(FILE_NAME) as data:
    train = data['train']
    train_labels = data['train_labels']
    knn = cv2.ml.KNearest_create()
    knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)



def check(test, train, train_labels):
# 가장 가까운 K개의 글자를 찾아, 어떤 숫자에 해당하는지 찾습니다.( 테스트 데이터 개수에 따라서 조절)
    ret, result, neighbours, dist = knn.findNearest(test, k=1)
    return result

def get_result(file_name):
    image = cv2.imread(file_name)
    chars = utils.extract_chars(image)
    result_string = ""
    for char in chars:
        matched = check(utils.resize20(char[1]), train, train_labels)
        if matched <10:
            result_string += str(int(matched))
            continue
        if matched ==10 :
            matched ='+'
        elif matched ==11:
            matched ='-'
        elif matched ==12:
            matched = '*'
        result_string += matched
    return result_string


print(get_result("2.png")) # 실제로 이미지로부터 수식정보 불러오기

host="http://localhost:10000"
url='/start'

#target_images 라는 폴더 생성
with requests.Session() as s:
    answer =''
    for i in range(0,100): #백개의 문제를 처리하기 위
        start_time = time.time()
        params={'ans':answer} #ans에 answer값을 넣어 서버로 제출하기 위

        #정답을 파라미터에 달아서 전송하여, 이미지 경로를 받아옵니다.
        response = s.post(host+url, params) #설정된 주소로 접속하여 리턴값을 받아
        print('Server Return: ' +response.text) #
        if i == 0: #호스트에서 가장 처음 리턴값을 받아올 때,
            returned = response.text    #가장처음 리턴값은 이미지url이므로 바로 저장
            image_url = host + returned
            url = '/check'
        else:#처음 이후의 리턴값은 json형태로 리턴값을 준다.
            returned = response.json() #따라서 json을 받아옴
            image_url = host + returned['url'] # json자료형중 url 키에 해당하는 값을 받아옴
        print ('Problem ' + str(i) + ': ' + image_url)

        #특정한 폴더에 이미지 파일을 다운로드 받습니다.
        response = s.get(image_url, stream = True)
        target_image = './target_images/' +str(i) + '.png'
        with open(target_image, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


        #다운로드 받은 이미지 파일을 분석하여 답을 도출합니다.
        answer_string=get_result(target_image)
        print('String: ' +answer_string)
        answer_string = utils.remove_first_0(answer_string)
        answer  = str(eval(answer_string)) #eval함수를 통 문자열수식을 계
        print('Answer: ' + answer)
        print("--- %s seconds ---" %(time.time() - start_time))