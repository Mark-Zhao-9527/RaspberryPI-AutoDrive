#-*-coding:utf-8-*-
#!/usr/bin/env python
#赵贵生：一起来玩树莓派5——树莓派机器人自动驾驶
#编写时间：2016.07.31
#引入autonomy函数，产生0-4之间随机数。随时数为0时测试前方距离。前过TF秒，1为原地左转。2为右转。2为左旋
#通过distance子程序没距离，小于15cm倒退2S。如果前方还太近，原地左转3S，还太近，退出程序

import RPi.GPIO as gpio  #第一行引用后，可以设置中文注释
import time
import sys
import random

gpio.setwarnings(False)   #去掉一些不必要的警告
zuoqian = 7               #7脚为控制左侧轮前进，11脚控制左侧轮子后退
zuohou = 11
youqian = 15              #15脚为控制右侧轮前进，13脚控制右侧轮子后退
youhou = 13

def init():
    gpio.setmode(gpio.BOARD) #GPIO调用BOARD编号方式
    gpio.setup(7,gpio.OUT)
    gpio.setup(11,gpio.OUT)
    gpio.setup(13,gpio.OUT)
    gpio.setup(15,gpio.OUT)
    gpio.setup(12,gpio.OUT)
    gpio.setup(16,gpio.IN)

def qianjin(timerun):     #左右都往前，为前进
    gpio.output(7,True)   #左侧轮子前进
    gpio.output(11,False)
    gpio.output(15,True)  #右侧轮子前进
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()         #演示timerum秒转动停止转动

def houtui(timerun):       #左右都往后，为前后
    gpio.output(7,False)   #左侧轮子后退
    gpio.output(11,True)
    gpio.output(15,False)  #右侧轮子后退
    gpio.output(13,True)
    time.sleep(timerun)
    gpio.cleanup()

def zuozhuan(timerun):     #左轮不动，右轮前进，为左转
    gpio.output(7,False)   #左侧轮子不动
    gpio.output(11,False)
    gpio.output(15,True)   #右侧轮子前进
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()         #演示timerum秒转动停止转动

def youzhuan(timerun):     #左轮前进，右轮不动，为右转
    gpio.output(7,True)    #左侧轮子前进
    gpio.output(11,False)
    gpio.output(15,False)  #右侧轮子不动
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()
def zuoxuan(timerun):      #左轮后退，右轮前进，为左旋转
    gpio.output(7,False)   #左侧轮子后退
    gpio.output(11,True)
    gpio.output(15,True)   #右侧轮子前进
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()

def youxuan(timerun):      #左轮前进，右轮后退，为右旋转
    gpio.output(7,True)    #左侧轮子前进
    gpio.output(11,False)
    gpio.output(15,False)  #右侧轮子后退
    gpio.output(13,True)
    time.sleep(timerun)
    gpio.cleanup()

def tingzhi(timerun):      #刹车不走了
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(15,False)
    gpio.output(13,False)
    time.sleep(timerun)
    gpio.cleanup()


def distance():
    init()

    gpio.output(12,True)  #发出触发信号保持10us以上（15us）
    time.sleep(0.000015)
    gpio.output(12,False)
    while not gpio.input(16):
        pass
    t1 = time.time()              #发现高电平时开时计时
    while gpio.input(16):
        pass
    t2 = time.time()              #高电平结束停止计时

    return (t2-t1)*34000/2        #返回距离，单位为厘米
    gpio.cleanup()
    return distance

def check_front():
    init()
    dist = distance()

    if dist < 15:
       print('close',dist)
       init()
       houtui(1)           #速度大快后退1S足够
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
       qianjin(0.2)      #前进的时间稍微长一些，效果好一点
       print '前进程序被执行。现在地距离是: %0.2f cm' %distance()
    elif x==1:
         check_front()
         init()
         zuoxuan(0.2)
         print '后退程序被执行。现在地距离是: %0.2f cm' %distance()
    elif x==2:
         check_front()
         init()
         youxuan(tf)
         print '后退程序被执行。现在地距离是: %0.2f cm' %distance()
    elif x==3:
         check_front()
         init()
         zuozhuan(tf)
         print '左转程序被执行。现在地距离是: %0.2f cm' %distance()
    elif x==4:
         check_front()
         init()
         youzhuan(tf)
         print '右转程序被执行。现在地距离是: %0.2f cm' %distance()

try:
    while True:
          autonomy()
except KeyboardInterrupt:
    gpio.cleanup()



























