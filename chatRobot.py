#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from setenv import env_chatrobot_key, env_chatrobot_userid 

class chatAIRobot:
    def __init__(self):
        self.Key = env_chatrobot_key
        self.userid = env_chatrobot_userid
        self.apiUrl = 'http://www.tuling123.com/openapi/api'

    def chat_response(self, msg):
        self.postdata = {
        'key'    : self.Key,
        'info'   : msg,
        'userid' : self.userid,
        }

        try:
            r = requests.post(self.apiUrl, data=self.postdata).json()
            return r.get('text')  
        except:
            # 将会返回一个None
            return