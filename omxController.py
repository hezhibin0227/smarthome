#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
from tinytag import TinyTag  # 获取MP3的播放时长
from pykeyboard import PyKeyboard  # 模拟键盘输入控制omxplayer


def createMP3List(mp3Path):
    myMP3List = {}
    index = 0
    files = os.listdir(mp3Path)
    for name in files:
        fullname = os.path.join(mp3Path, name)
        if (name.endswith('.mp3')):
            tag = TinyTag.get(fullname)  # 获取MP3的播放时长
            mp3info = []
            mp3info.append(fullname)  # 将路径+文件名填入MP3信息List
            mp3info.append(tag.duration)  # 将播放时长填入MP3信息List
            myMP3List[index] = mp3info  # 将MP3信息List填入播放列表Dictionary的当前键下
            index += 1
    return myMP3List


class omxplayer:
    def __init__(self, mp3Path):
        self.playerbin = '/usr/bin/omxplayer -o alsa '
        self.keyboard = PyKeyboard()
        self.mp3List = createMP3List(mp3Path)

    def pstop(self, delay):
        time.sleep(delay)
        #self.keyboard.tap_key('q')  # 退出omxplayer
        str = "killall -9 omxplayer.bin"
        os.system(str)  # 退出omxplayer
        print ("["+ __name__ + "] Log >> " + u'[omxplayer] quit')
        time.sleep(1)

    def pvolumeUp(self):
        self.keyboard.tap_key('+', n=3, interval=1)  # 增大音量
        print ("["+ __name__ + "] Log >> " + u'[omxplayer] volume +')
        time.sleep(1)


    def pvolumeDown(self):
        self.keyboard.tap_key('-', n=3, interval=1)  # 减小音量
        print ("["+ __name__ + "] Log >> " + u'[omxplayer] volume -')
        time.sleep(1)

    def pplay(self, index):
        self.pstop(0.1)
        str = self.playerbin + self.mp3List[index][0]
        os.system(str)  # 播放第<index>首歌曲
        print "["+ __name__ + "] Log >> " + u'[omxplayer] play', index, ' MP3'
        time.sleep(1)

##########################testing#################################
if __name__ == "__main__":
    try:
        myPlayer = omxplayer('/home/pi/Music')
        thread.start_new_thread(myPlayer.pplay, (4,))
        print ("["+ __name__ + "] Log >> " + "pvolumeDown begin")
        thread.start_new_thread(myPlayer.pvolumeDown, ())
        print ("["+ __name__ + "] Log >> " + "pvolumeDown end")
        thread.start_new_thread(myPlayer.pstop, (10,))

    except:
        print ("["+ __name__ + "] Log >> " + "Error: unable to start thread")

    while 1:
        pass

