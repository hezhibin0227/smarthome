#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
from redisStore import redisDB
import time
import datetime

class DHT11Reader:
    def __init__(self):
        self.channel = 18  # GPIO24
        self.myRedis = redisDB()

    def read_data_once(self):
        #########################################
        ### ͨ�������߷���DTH11�Ķ�дЭ��˳�� ###
        ## 1.��������ʼ�ź�
        ## 2.�����ȴ�����DHT11��Ӧ�ź�
        ## 3.������������40 Bit�����ݺ�У���
        ## 4.���ݴ���
        #########################################

        data = []                            # DHT11���ݰ�
        j = 0                                # ��ȡbit������

        GPIO.setmode(GPIO.BOARD)
        time.sleep(1) 

        GPIO.setup(self.channel, GPIO.OUT)   # ���øö˿�Ϊ���
        GPIO.output(self.channel, GPIO.LOW)  # �û���������һ�ο�ʼ�źţ��͵�ƽ��
        time.sleep(0.02)                     # ���߱�����������18���룬��֤DTH11�ܼ�⵽��ʼ�ź�
        GPIO.output(self.channel, GPIO.HIGH) # ������ʼ�źŽ������ߵ�ƽ����Ȼ�������ʱ�ȴ�20-40΢�룬��
        GPIO.setup(self.channel, GPIO.IN)    # ��ȡDHT11�Ļ�Ӧ�ź�

        while GPIO.input(self.channel) == GPIO.LOW:      # ��ȡ����Ϊ�͵�ƽ��˵��DHT11��������Ӧ�ź�  
            continue  
        while GPIO.input(self.channel) == GPIO.HIGH:     # DHT11������Ӧ�źź����������ߣ�׼���������� 
            continue  
        while j < 40:                                    # DHT11�����ݰ���СΪ5��bytes(40��bit)��ѭ����ȡ40��bit   
            k = 0  
            while GPIO.input(self.channel) == GPIO.LOW:  # ����DHT11���ݣ�����DHT11�Ȱ���������12-14΢��
                 continue  
            while GPIO.input(self.channel) == GPIO.HIGH: # Ȼ������  
                k += 1  
                if k > 100:  
                    break  

            if k < 8:                       # �����ߵ�ƽ����ʱ����26-28΢�������Χ��
                data.append(0)              # ���bitΪ'0'��ƽ
            else:                           # �����ߵ�ƽ����ʱ����116-118΢�������Χ��
                data.append(1)              # ���bitΪ'1'��ƽ
            j += 1  

        humidity_bit = data[0:8]            # ʪ�ȵ��������֣������ƣ�  
        humidity_point_bit = data[8:16]     # ʪ�ȵ�С�����֣������ƣ� 
        temperature_bit = data[16:24]       # �¶ȵ��������֣������ƣ�
        temperature_point_bit = data[24:32] # �¶ȵ�С�����֣������ƣ�
        check_bit = data[32:40]             # У��ͣ������ƣ�  

        humidity = 0  
        humidity_point = 0  
        temperature = 0  
        temperature_point = 0  
        check = 0  

        for i in range(8):                  # ������תʮ����
            humidity += humidity_bit[i] * 2 ** (7-i)  
            humidity_point += humidity_point_bit[i] * 2 ** (7-i)  
            temperature += temperature_bit[i] * 2 ** (7-i)  
            temperature_point += temperature_point_bit[i] * 2 ** (7-i)  
            check += check_bit[i] * 2 ** (7-i)  

        tmp = humidity + humidity_point + temperature + temperature_point  # ����У���
         

        if check == tmp:  # �����У���һ�£�˵������Ч����
            print "["+ __name__ + "] Log >> " + "temperature :", temperature, "*C, humidity :", humidity, "%"  
            time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            redis_record = time_string + '|'+ str(temperature) + '|' + str(humidity)
            self.myRedis.session.lpush('DHT11List', redis_record)
            if self.myRedis.session.llen('DHT11List') > 20:  
                self.myRedis.session.ltrim('DHT11List',0,19)  # �����20����������

        else:  
            print "["+ __name__ + "] Log >> " + "Wrong data"  
            print "["+ __name__ + "] Log >> " + "temperature :", temperature, "*C, humidity :", humidity, "% check :", check, ", tmp :", tmp  
  
        #GPIO.cleanup()  

if __name__ == "__main__":
    myDHT11 = DHT11Reader()

    try:  
        while True:  
            myDHT11.read_data_once()
            time.sleep(5)  # ÿ5���Ӷ�ȡһ������
    except KeyboardInterrupt:  
        GPIO.cleanup()


    