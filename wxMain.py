#!/usr/bin/python
# -*- coding: UTF-8 -*-

import itchat
from itchat.content import *
from chatRobot import chatAIRobot
from messageHandler import wxHandler
from objStore import ecsTestDrive
from setenv import env_obj_url

myAIRobot = chatAIRobot()  # 初始化AI聊天机器人
mywxHandler = wxHandler()  # 初始化微信消息控制器
myObjStore = ecsTestDrive()  # 初始化ECS Test Drive Boto接口

AI_ON = False  # 缺省关闭AI聊天机器人

################# 处理微信消息 ####################
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg['Text']
    defaultReply = 'wxMain received: ' + text  # 设置默认回复
    print("["+ __name__ + "] Log >> " + defaultReply)
    global AI_ON
        
    if text.upper() == "AION":
        AI_ON = True
        return "AI chat robot is active"
    elif text.upper() == "AIOFF":
        AI_ON = False
        return "AI chat robot is inactive"
    elif text.upper() == "QUIT":
        mywxHandler.msg_handler('QUIT')  # 清理资源: GPIO/omxplayer
        itchat.logout()
        return "Quit now!"
    else:
        pass
    
    if AI_ON:
        reply = myAIRobot.chat_response(text)  # AI机器人自动聊天应答
        return reply or defaultReply
    else:
        reply = mywxHandler.msg_handler(text)  # 控制树莓派播放MP3
        return reply or defaultReply
        return defaultReply

#################处理微信附件: 图片/语音/视频/文件####################
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def upload_files(msg):
    msg.download(msg.fileName)
    print("["+ __name__ + "] Log >> " + "msg.filename = " +  msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', 
        RECORDING: 'rec',
        ATTACHMENT: 'att',}.get(msg.type, 'fil')
    print("["+ __name__ + "] Log >> " + "msg.type = " +  typeSymbol)
    myObjStore.upload_to_ecs(msg.fileName, typeSymbol)
    
    return "This object has been uploaded to ECS Test Drive and its URL is: " + env_obj_url + msg.fileName
    #return '@%s@%s' % (typeSymbol, msg.fileName)

################# 微信登录 ####################
itchat.auto_login(hotReload=True)
itchat.run(debug=True)