#!/usr/bin/python
# -*- coding: UTF-8 -*-

import redis
from setenv import env_redis_host, env_redis_port, env_redis_password

class redisDB:
    def __init__(self):
        self.redis_host = env_redis_host  
        self.redis_port = env_redis_port
        self.redis_password = env_redis_password

        self.session = redis.Redis(host=self.redis_host, port=self.redis_port, password=self.redis_password)
        print("["+ __name__ + "] Log >> " +  "connected to redis on PWS")
       
    def update_led_status(self, R, G, B):
        self.session.hmset('ledhash', {'RED':R, 'GREEN': G, 'BLUE': B})

    def read_led_status(self):
        return self.session.hmget('ledhash','RED','GREEN','BLUE')

    def read_content(self):
        content = {'time0':'', 'temp0':'', 'humd0':'',
                   'time1':'', 'temp1':'', 'humd1':'',
                   'time2':'', 'temp2':'', 'humd2':'',
                   'RED':'', 'GREEN':'', 'BLUE':''}
        recordList = self.session.lrange('DHT11List',0,2)
        status_list = recordList[0].split('|')
        content['time0']=status_list[0]
        content['temp0']=status_list[1]
        content['humd0']=status_list[2]
        status_list = recordList[1].split('|')
        content['time1']=status_list[0]
        content['temp1']=status_list[1]
        content['humd1']=status_list[2]
        status_list = recordList[2].split('|')
        content['time2']=status_list[0]
        content['temp2']=status_list[1]
        content['humd2']=status_list[2]

        ledList = self.read_led_status()
        content['RED']=ledList[0]
        content['GREEN']=ledList[1]
        content['BLUE']=ledList[2]
        return content

if __name__ == "__main__":
    myRedis = redisDB()

    ### populate the testing data ###
    ### lpush the timestamp, temperature & humidity data into DHT11List ###
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:00|24.00|75')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:01|24.01|76')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:02|24.02|77')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:03|24.03|78')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:04|24.04|79')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:05|24.05|80')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:06|24.06|81')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:07|24.07|82')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:08|24.08|83')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:09|24.09|84')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:10|24.10|85')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:11|24.11|86')
    myRedis.session.lpush('DHT11List','2018-02-27 12:08:12|24.12|87')

    if myRedis.session.llen('DHT11List') > 10:
        myRedis.session.ltrim('DHT11List',0,9)
    
    myRedis.update_led_status(True, False, False)

    print("["+ __name__ + "] Log >> " + myRedis.read_content())

