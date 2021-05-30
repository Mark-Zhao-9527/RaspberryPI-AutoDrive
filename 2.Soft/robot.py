#-*-coding:utf-8-*-
#!/usr/bin/env python
#�Թ�����һ��������ݮ��5������ݮ�ɻ������Զ���ʻ
#��дʱ�䣺2016.07.31
#����autonomy����������0-4֮�����������ʱ��Ϊ0ʱ����ǰ�����롣ǰ��TF�룬1Ϊԭ����ת��2Ϊ��ת��2Ϊ����
#ͨ��distance�ӳ���û���룬С��15cm����2S�����ǰ����̫����ԭ����ת3S����̫�����˳�����

import RPi.GPIO as gpio  #��һ�����ú󣬿�����������ע��
import time
import sys
import random

gpio.setwarnings(False)   #ȥ��һЩ����Ҫ�ľ���
zuoqian = 7               #7��Ϊ���������ǰ����11�ſ���������Ӻ���
zuohou = 11
youqian = 15              #15��Ϊ�����Ҳ���ǰ����13�ſ����Ҳ����Ӻ���
youhou = 13

def init():
    gpio.setmode(gpio.BOARD) #GPIO����BOARD��ŷ�ʽ
    gpio.setup(7,gpio.OUT)
    gpio.setup(11,gpio.OUT)
    gpio.setup(13,gpio.OUT)
    gpio.setup(15,gpio.OUT)
    gpio.setup(12,gpio.OUT)
    gpio.setup(16,gpio.IN)

def qianjin(timerun):     #���Ҷ���ǰ��Ϊǰ��
    gpio.output(7,True)   #�������ǰ��
    gpio.output(11,False)
    gpio.output(15,True)  #�Ҳ�����ǰ��
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()         #��ʾtimerum��ת��ֹͣת��

def houtui(timerun):       #���Ҷ�����Ϊǰ��
    gpio.output(7,False)   #������Ӻ���
    gpio.output(11,True)
    gpio.output(15,False)  #�Ҳ����Ӻ���
    gpio.output(13,True)
    time.sleep(timerun)
    gpio.cleanup()

def zuozhuan(timerun):     #���ֲ���������ǰ����Ϊ��ת
    gpio.output(7,False)   #������Ӳ���
    gpio.output(11,False)
    gpio.output(15,True)   #�Ҳ�����ǰ��
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()         #��ʾtimerum��ת��ֹͣת��

def youzhuan(timerun):     #����ǰ�������ֲ�����Ϊ��ת
    gpio.output(7,True)    #�������ǰ��
    gpio.output(11,False)
    gpio.output(15,False)  #�Ҳ����Ӳ���
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()
def zuoxuan(timerun):      #���ֺ��ˣ�����ǰ����Ϊ����ת
    gpio.output(7,False)   #������Ӻ���
    gpio.output(11,True)
    gpio.output(15,True)   #�Ҳ�����ǰ��
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()

def youxuan(timerun):      #����ǰ�������ֺ��ˣ�Ϊ����ת
    gpio.output(7,True)    #�������ǰ��
    gpio.output(11,False)
    gpio.output(15,False)  #�Ҳ����Ӻ���
    gpio.output(13,True)
    time.sleep(timerun)
    gpio.cleanup()

def tingzhi(timerun):      #ɲ��������
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(15,False)
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()


def distance():
    init()

    gpio.output(12,True)  #���������źű���10us���ϣ�15us��
    time.sleep(0.000015)
    gpio.output(12,False)
    while not gpio.input(16):
        pass
    t1 = time.time()              #���ָߵ�ƽʱ��ʱ��ʱ
    while gpio.input(16):
        pass
    t2 = time.time()              #�ߵ�ƽ����ֹͣ��ʱ

    return (t2-t1)*34000/2        #���ؾ��룬��λΪ����
    gpio.cleanup()
    return distance

def check_front():
    init()
    dist = distance()

    if dist < 15:
       print('close',dist)
       init()
       houtui(1)           #�ٶȴ�����1S�㹻
       init()
       dist = distance()
       if dist < 15:
          print('too close',dist)
          init()
          zuoxuan(3)
          init()
          houtui(1)
          dist = distance()
          if dist<15:
             print('too too close',dist)
             tingzhi(2)

def autonomy():
    tf = 0.1
    x = random.randrange(0,5)

    if x==0:
       check_front()
       init()
       qianjin(0.2)      #ǰ����ʱ����΢��һЩ��Ч����һ��
       print 'ǰ������ִ�С����ڵؾ�����: %0.2f cm' %distance()
    elif x==1:
         check_front()
         init()
         zuoxuan(0.2)
         print '���˳���ִ�С����ڵؾ�����: %0.2f cm' %distance()
    elif x==2:
         check_front()
         init()
         youxuan(tf)
         print '���˳���ִ�С����ڵؾ�����: %0.2f cm' %distance()
    elif x==3:
         check_front()
         init()
         zuozhuan(tf)
         print '��ת����ִ�С����ڵؾ�����: %0.2f cm' %distance()
    elif x==4:
         check_front()
         init()
         youzhuan(tf)
         print '��ת����ִ�С����ڵؾ�����: %0.2f cm' %distance()

try:
    while True:
          autonomy()
except KeyboardInterrupt:
    gpio.cleanup()



























