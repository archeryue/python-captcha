#!/usr/bin/python
# -*- coding: utf8 -*-

# author: yuzhengyang

import sys
import pytesseract
from PIL import Image,ImageDraw


#二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
#该函数也可以改成RGB判断的,具体看需求如何
def getPixel(image,x,y,G,N):
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x,y-1))
    else:
        return None

# 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image,G,N,Z):
    draw = ImageDraw.Draw(image)

    for i in xrange(0,Z):
        for x in xrange(1,image.size[0] - 1):
            for y in xrange(1,image.size[1] - 1):
                color = getPixel(image,x,y,G,N)
                if color != None:
                    draw.point((x,y),color)

def initTable(threshold=140):
 table = []
 for i in range(256):
     if i < threshold:
         table.append(0)
     else:
         table.append(1)

 return table

def get_letter_array(img):
    inletter = False
    foundletter=False
    start = 0
    end = 0
    letters = []
    for x in range(img.size[0]):
        count = 0
        hit = False
        for y in range(img.size[1]):
            pix = img.getpixel((x,y))
            if pix != 1:
                if hit:
                    count += 1
                hit = True
            else:
                hit = False
        if count > 0:
            inletter = True
        if foundletter == False and inletter == True:
            foundletter = True
            start = x
        if foundletter == True and inletter == False:
            foundletter = False
            end = x
            letters.append((start,end))
        inletter=False
    print letters
    return letters

def split_image(img):
    res = []
    for letter in get_letter_array(img):
        sub_img = img.crop((letter[0], 0, letter[1], img.size[1]))
        res.append(sub_img)
    return res

def handle(path):
    pic = Image.open(path).convert('L')
    clearNoise(pic, 140, 4, 2)
    # pic.show()
    binaryImage = pic.point(initTable(), '1')
    binaryImage.show()
    # pic.save('gray.png')
    alphas = split_image(binaryImage)
    print pytesseract.image_to_string(binaryImage, config='-psm 7')
    res_str = ''
    for alpha in alphas:
        # alpha.show()
        res_str += pytesseract.image_to_string(alpha, config='-psm 10')
    print res_str

if __name__ == '__main__':
    path = str(sys.argv[1])
    handle(path)
