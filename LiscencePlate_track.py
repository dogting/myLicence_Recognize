# !/user/bin/env python
# -*- coding:utf-8 -*-

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
import cv2
import re
import HyperLPRLite as pr


class track():
    def __init__(self):
        self.model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
        print('init')
        pass

    def drawRectBox(self,image, rect, addText):
        fontC = ImageFont.truetype("./Font/platech.ttf", 14, 0)
        cv2.rectangle(image, (int(rect[0] - 1), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                      (0, 0, 255), 2, cv2.LINE_AA)
        cv2.rectangle(image, (int(rect[0] - 2), int(rect[1]) - 16), (int(rect[0] + 115), int(rect[1])), (0, 0, 255), -1,
                      cv2.LINE_AA)
        img = Image.fromarray(image)
        # print("test:" + addText)
        draw = ImageDraw.Draw(img)
        # draw.text((int(rect[0]+1), int(rect[1]-16)), addText.decode("utf-8"), (255, 255, 255), font=fontC)
        draw.text((int(rect[0] + 1), int(rect[1] - 16)), addText, (255, 255, 255), font=fontC)
        imagex = np.array(img)
        return imagex

    def LP_infom(self,grr):
        inform = {}

        result =  self.model.SimpleRecognizePlateByE2E(grr)
        for pstr, confidence, rect in result:
            if confidence > 0.7:
                image = self.drawRectBox(grr, rect, pstr+" "+str(round(confidence,3)))
                grr = image
                province = re.search(r'[\u4E00-\u9fa5]+',pstr)
                if province is None:
                    continue
                    province = ""
                platenum = re.sub(r'[\u4E00-\u9fa5]+','', pstr)
                # car = Carinform(pstr,[int(x) for x in rect]).get_CarInform()
                car = Carinform(pstr, [int(x) for x in rect])
                inform[platenum] = car  #存储车牌对应的坐标，如：{‘车牌数字号码’：car对象}

        return inform
# if __name__ == '__main__':
#     grr = cv2.imread(r"D:\CMCC\License_plate\HyperLPR-master\1.png")
#     inform=LiscencePlate_track().LP_infom(grr)
#     print(inform)
#-------------------车对象------------------
class Carinform:
    def __init__(self,liscencePlate,rect,speed='',time='',endtime='',filePath=''):


        self.__liscencePlate = liscencePlate
        self.__speed = speed
        self.__rect = rect
        self.__time = time
        self.__endtime = endtime
        self.__filePath = filePath

    def set_CarInform(self,liscencePlate,rect,speed='',time='',endtime='',filePath=''):
        self.__liscencePlate = liscencePlate
        self.__speed = speed
        self.__rect = rect
        self.__time = time
        self.__endtime = endtime
        self.__filePath = filePath
    def set_filePath(self,filePath):
        self.__filePath = filePath
    def get_filePath(self):
        return self.__filePath
    def get_CarInform(self):
        return self.__liscencePlate,self.__rect,self.__time,self.__endtime,self.__speed,self.__filePath

    def set_LiscencePlate(self,liscencePlate):
        self.__liscencePlate=liscencePlate
    def get_LiscencePlate(self):
        return self.__liscencePlate
    def set_EndTime(self,endtime):
        self.__endtime = endtime
    def get_EndTime(self):
        return self.__endtime
    def set_Speed(self,speed):
        self.__speed = speed
    def get_Speed(self):
        return self.__speed
    def set_Rect(self,rect):
        self.__rect = rect
    def get_Rect(self):
        return self.__rect
    def set_Time(self,time):
        self.__time = time
    def get_Time(self):
        return self.__time