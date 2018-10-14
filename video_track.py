# !/user/bin/env python
# -*- coding:utf-8 -*-

import cv2
import imageio
import LiscencePlate_track
import SQL_Store
from VideoGUI import *
import re
from PIL import Image
import numpy as np



from moviepy.editor import VideoFileClip
imageio.plugins.ffmpeg.download()
class video_track(QMainWindow,Ui_MainWindow):
    message = ""
    def __init__(self,form,videoPathRead="", parent=None):
        super(video_track, self).__init__(parent)
        self.setupUi(self)
        # self.videoPathRead = 'D:\CMCC\License_plate\HyperLPR-master\HyperLPR-master/car.mov'
        self.videoPathRead = videoPathRead
        self.videoPathWrite = 'D:\CMCC\License_plate\HyperLPR-master\HyperLPR-master/car_te.mov'
        self.timedelay = 60
        self.form=form

        self.cap = cv2.VideoCapture(self.videoPathRead)  # 读取视频
        pass

    def log(self,data):
        self.form.Signal_Log.emit(str(data))

    def process_image(self,image, mwidth=600, mheight=700):

        w, h = image.size
        if (1.0 * w / mwidth) > (1.0 * h / mheight):
            scale = 1.0 * w / mwidth
            new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)

        else:
            scale = 1.0 * h / mheight
            new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        return  new_im

    #找到车辆，显示找到特定的帧的图片
    def find_car(self,string):

        if len(str(string).split(';')) > 1:
            begintime  = str(string).split(';')[4]
            begintime = int(re.search( r'\d+', begintime).group())
            endtime =  str(string).split(';')[5]
            endtime = int(re.search(r'\d+', endtime).group())
            if endtime !=None:
                cartime = int(endtime)
            else:
                cartime = int(begintime)
            rectList =  str(string).split(';')[3].split(r',')
            rect = []
            for rectstring in rectList:
                rect.append(int(re.search(r'\d+', rectstring).group()))
            # licensePlate = str(string).split(';')[2].split('=')[2]
            #获取特定帧的图片
            self.videoPathRead = str(string).split(';')[7].split('=')[1]
            pattern = re.compile('\'(.*)\'')
            self.videoPathRead = pattern.findall(self.videoPathRead)
            self.cap = cv2.VideoCapture(self.videoPathRead[0])

            self.cap.set(cv2.CAP_PROP_POS_FRAMES, cartime)
            ret, frame = self.cap.read()


            if ret:
                 cv2.rectangle(frame, (int(rect[0] - 1), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                               (0, 0, 255), 2, cv2.LINE_AA)
            img = Image.fromarray(frame)


            img = self.process_image(img)
            imagex = np.array(img)
            cv2.imwrite('a.jpg',imagex)


            self.log(string+"&show")
        else:
            self.log(string)


    def get_video(self,cameraID):
        # video handle
        # cap = VideoFileClip(self.videoPathRead).subclip(0.00,5)
        # cap.write_videofile('D:\CMCC\License_plate\HyperLPR-master\HyperLPR-master/car_short.mp4', audio=False)
        # if True:
        #     return True


        frames_num = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))  # 读取视频FPS值
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # 读取视频大小
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc =cv2.VideoWriter_fourcc(*"mp4v")  # 编码方式
        videoWriter1 = cv2.VideoWriter(self.videoPathWrite, fourcc, fps, size)  # 创建写入对象
        ret, frame = self.cap.read()  # 读取视频
        traker = LiscencePlate_track.track()
        SQL = SQL_Store.SQL_store()
        timecount = 0
        Carnum={}
        while ret:

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            timecount += 1
            if timecount >= frames_num:
                self.message += '100%'+'\r\n'+'finished'
                self.log(self.message)
                break
            if timecount%self.timedelay == 0:
                # image_np  = cv2.imencode('.jpg', frame)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, timecount)
                ret, frame = self.cap.read()
                image_np = frame

                #-------user code--------------
                inform = traker.LP_infom(image_np)

                for key in inform:

                    image_np = traker.drawRectBox(image_np,inform[key].get_CarInform()[1],inform[key].get_CarInform()[0])


                    #插入车辆信息
                    inform[key].set_Time(str(timecount))
                    inform[key].set_EndTime(str(timecount))
                    inform[key].set_filePath(str(self.videoPathRead))
                    # self.message += str(inform[key].get_CarInform())+"\r\n" #车牌信息显示
                    # self.log(self.message)
                    SQL.InsertData('car', inform[key].get_CarInform(),cameraID)

                    # Carnum[key] = "" #用于计算车辆数目
                videoWriter1.write(image_np)
                self.message = str(int(timecount*100/frames_num))+"%" + "\r\n"  # 车牌信息显示
                self.log(self.message)


            #-------read video-------------
            # ret, frame = cap.read()
        self.cap.release()
        cv2.destroyAllWindows()
