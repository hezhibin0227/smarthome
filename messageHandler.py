#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
from omxController import omxplayer
from RGBController import RGBLedSetter
from redisStore import redisDB
from setenv import env_mp3_location
import sys
if sys.getdefaultencoding()!='utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

class wxHandler:
    def __init__(self):
        self.help_msg = \
            u"H:---------HELP\n" \
            u"L:----------List of songs\n" \
            u"P [n]:-----Play the nth song\n" \
            u"S:----------Stop play\n"\
            u"T:----------Temperature\n"\
            u"D:---------Humdity\n"\
            u"R:---------RED LED on\n"\
            u"G:---------GREEN LED on\n"\
            u"B:---------BLUE LED on\n"\
            u"O:---------LED off\n"\
            u"AION:----AI chat on\n"\
            u"AIOFF:---AI chat off\n"\
            u"<File>:---Upload File\n"
        self.myPlayer = omxplayer(env_mp3_location)  # 初始化omxplayer
        self.mp3index = 0  # 播放列表指针，默认指向第0首
        self.myLedSetter = RGBLedSetter()  # 初始化LED Controller
        self.myRedis = redisDB()  # 初始化Redis读取器


    def msg_handler(self, args):
        print ("["+ __name__ + "] Log >> " + "Received message is: " + args)
        arg_list = args.split(" ")  # 参数以空格为分割符
        res = "Improper input, please refer to:\n" + self.help_msg
        if len(arg_list) == 1:  # 如果参数数量为1个 (H/L/P/S/+/-/R/G/B/O)
            arg = arg_list[0]
            if arg.upper() == u'H':  # 帮助信息
                res = self.help_msg
            elif arg.upper() == u'L':  # 歌曲列表
                if len(self.myPlayer.mp3List) == 0:
                    res = "The song list is empty"
                else:
                    res = ""
                    for i in range(len(self.myPlayer.mp3List)):
                        res += str(i) + ". " + self.myPlayer.mp3List[i][0][15:] + "\n"
                    res += "\nInput \"P [n]\" to play nth song"
            elif arg.upper() == u'P':  # 不加序号，默认播放第0首歌曲
                if len(self.myPlayer.mp3List) > 0:
                    self.mp3index = 0  # 播放顺序定位到第0首
                    #self.myPlayer.pplay(self.mp3index)
                    try:
                        thread.start_new_thread(self.myPlayer.pplay, (self.mp3index,))
                    except:
                        print ("["+ __name__ + "] Log >> " + "Error: unable to start thread for P")
                    res = "Playing: " + self.myPlayer.mp3List[self.mp3index][0][15:]  # 播放第0首歌曲
                else:
                    res = "The song list is empty"
            elif arg.upper() == u'S':  # 停止播放
                self.myPlayer.pstop(0.1)
                res = "Play stopped"
            elif arg.upper() == u'T':  # 温度
                content = self.myRedis.read_content()
                res = content['time0'] + "\n\nTemperature is: " + content['temp0'] + "℃" 
            elif arg.upper() == u'D':  # 湿度
                content = self.myRedis.read_content()
                res = content['time0'] + "\n\nHumditiy is: " + content['humd0'] + "%"
            elif arg.upper() == u'R':  # LED显示红色
                self.myLedSetter.R_Led_on()
                res = "RED LED is On"
            elif arg.upper() == u'G':  # LED显示绿色
                self.myLedSetter.G_Led_on()
                res = "GREEN LED is On"
            elif arg.upper() == u'B':  # LED显示蓝色
                self.myLedSetter.B_Led_on()
                res = "BLUE LED is On"
            elif arg.upper() == u'O':  # LED关闭
                self.myLedSetter.all_Led_off()
                res = "LED is Off"
            elif arg.upper() == u'QUIT':  # 退出程序，清理资源
                self.myLedSetter.all_Led_off()
                self.myPlayer.pstop(0.1)
                res = "Resources is cleaned"
            else:
                res = "Improper input, please refer to:\n" + self.help_msg

        elif len(arg_list) == 2:  # 如果参数数量为2个: P [n]
            arg1 = arg_list[0]
            arg2 = arg_list[1]
            if arg1 == u'P' or arg1 == u'p' :
                if len(self.myPlayer.mp3List) > 0:
                    if arg2.isdigit():  # n是数字
                        if int(arg2) >= 0 and int(arg2) <= len(self.myPlayer.mp3List):  # n在正常范围内
                            self.mp3index = int(arg2)
                            #self.myPlayer.pplay(self.mp3index)
                            try:
                                thread.start_new_thread(self.myPlayer.pplay, (self.mp3index,))
                            except:
                                print ("["+ __name__ + "] Log >> " + "Error: unable to start thread for P [n]")
                            res = "Playing: " + self.myPlayer.mp3List[self.mp3index][0][15:]  # 播放第n首歌曲
                    else:
                        res = "Improper input, please refer to:\n" + self.help_msg
                else:
                    res = "The song list is empty"
        return res


