import cv2
import os
import numpy as np

file_names=list(range(0,13))
train=[]
train_labels=[]

for file_name in file_names:
    path='./training_data/' + str(file_name) + '/'
    file_count = len(next(os.walk(path))[2]) # 폴더 내 파일 개수 카운트
    for i in range(1, file_count + 1): # 파일 개수만큼 반복문
        img = cv2.imread(path + str(i) + '.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        train.append(gray)
        train_labels.append(file_name)

x=np.array(train)
train= x[:,:].reshape(-1,400).astype(np.float32)
train_labels = np.array(train_labels)[:, np.newaxis]

print(train.shape)
print(train_labels.shape) #개수 확인
print(train_labels) # 각 숫자들이 존재할 때마다 출력
np.savez("trained.npz",train = train, train_labels = train_labels)

