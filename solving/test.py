import cv2
import utils

#이미지를 불러옴
image=cv2.imread('1.png',cv2.IMREAD_COLOR)
#만들어놓은 utils 함수를 거쳐서 이미지를 정제
blue=utils.get_chars(image.copy(),utils.BLUE)
green=utils.get_chars(image.copy(),utils.GREEN)
red=utils.get_chars(image.copy(),utils.RED)

cv2.imshow('Image Gray',blue)
cv2.waitKey(0)
cv2.imshow('Image Gray',green)
cv2.waitKey(0)
cv2.imshow('Image Gray',red)
cv2.waitKey(0)
