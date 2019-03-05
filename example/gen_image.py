
#coding=utf-8
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
#conda install Pillow
from PIL import Image
import random
#pip install captcha 安装验证码库
from captcha.image import ImageCaptcha
 
#本代码生成验证码图片
number = ['0','1','2','3','4','5','6','7','8','9']  
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']  
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']  
 
def random_captcha_text(char_set=number+alphabet+ALPHABET, captcha_size=4):  
    captcha_text = []  
    for i in range(captcha_size):  
        c = random.choice(char_set)  
        captcha_text.append(c)  
    return captcha_text  
   
 
def gen_captcha_text_and_image():  
    #构造captcha对象
    char_set = number
    image = ImageCaptcha()  
   
    captcha_text = random_captcha_text(char_set=char_set)  
    #list->string
    captcha_text = ''.join(captcha_text)  
   #生成图像验证码
    captcha = image.generate(captcha_text)  
    #image.write(captcha_text, captcha_text + '.jpg')   
   
    captcha_image = Image.open(captcha)  
    #转换为numpu array格式
    captcha_image = np.array(captcha_image)  
    #返回Label和验证码
    return captcha_text, captcha_image  
if __name__ == '__main__':  
    text, image = gen_captcha_text_and_image()  
   
    f = plt.figure()  
    ax = f.add_subplot(111)  
    ax.text(0.1, 0.9,text, ha='center', va='center', transform=ax.transAxes)  
    plt.imshow(image)  
    plt.show() 