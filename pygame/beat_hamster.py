#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/12/16 18:53
# @Author   : Heyangyang
# 1、导入模块
import pygame
from pygame.locals import *
import math
import random

# 2、游戏初始化

# 2.1设置展示窗口
pygame.init()
width , height = 640 , 480
screen = pygame.display.set_mode((width,height))

# 2.2 游戏中需要用到的按键keys:wasd
keys = [False,False,False,False]

# 2.3 游戏玩家的初始位置
playerpos = [100,100]

# 2.4 跟踪箭头
arrows = []

# 2.5 记录玩家精度：消灭的獾的数量and射出的箭头数量
acc = [0,0]

# 2.6 添加坏蛋和坏蛋计时器（隔一段时间出来一个坏蛋）
badguys = [[640,100]]
badtimer = 100
badtimer1 = 0

# 2.7 初始健康值
healthvalue = 194

# 2.8 声音初始化
pygame.mixer.init()

# 3、导入声音和图片

# 3.1、导入展示的图片
player = pygame.image.load(r".\\pic_lib\dude2.png")
background = pygame.image.load(r".\\pic_lib\grass.png")
arrow = pygame.image.load(r".\\pic_lib\bullet.png")
badguyimg1 = pygame.image.load(r".\\pic_lib\badguy4.png")
badguyimg = badguyimg1    # 添加了一个图片的复制
castle = pygame.image.load(r".\\pic_lib\castle.png")
healthbar = pygame.image.load(r".\\pic_lib\healthbar.png")
health = pygame.image.load(r".\\pic_lib\health.png")
gameover = pygame.image.load(r".\\pic_lib\gameover.png")
youwin = pygame.image.load(r".\\pic_lib\youwin.png")

# 3.2、加载游戏操作的声音
hit = pygame.mixer.Sound(r".\\pic_lib\explode.wav")
enemy = pygame.mixer.Sound(r".\\pic_lib\enemy.wav")
shoot = pygame.mixer.Sound(r".\\pic_lib\shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)

# 3.3 加载背景音乐
pygame.mixer.music.load(r".\\pic_lib\moonlight.wav")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.25)

# 4、保持循环，游戏运行
running = 1
exitcode = 0
while running:
    badtimer -= 1
    # 5、clear the screen before drawing it again
    screen.fill(0)

    # 6、draw the screen element

    # 6.0 添加背景
    for x in range(round( width/background.get_width() ) +1):
        for y in range(round( height/background.get_height() ) +1):
            screen.blit(background,(x*100,y*100))
            # 图片小于背景

    # 6.1 添加castles
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345))


    # 6.2 添加玩家
    position = pygame.mouse.get_pos()
        # 获取鼠标位置
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        # 鼠标的位置和玩家的位置，根据三角定理，可得旋转角度函数为：atan2()
    playerrot = pygame.transform.rotate(player,360-angle*57.29)
        # 将玩家按所需角度旋转
    playerpos1 = (playerpos[0]+playerrot.get_rect().width/2, playerpos[1]+playerrot.get_rect().height/2)
        # 计算玩家旋转角度后的位置
    screen.blit(playerrot, playerpos1)
        # 玩家移动到鼠标指定位置

    # 6.3 添加箭头
    for projectile in arrows:
        arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
        screen.blit(arrow1, (projectile[1], projectile[2]))
    for bullet in arrows:
        index = 0
        vlex = math.cos(bullet[0])*10
        vley = math.sin(bullet[0])*10
            # 10 是箭头的速度
        bullet[1] += vlex
        bullet[2] += vley
        if  bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            # 如果超出屏幕，删除箭头
            arrows.pop(index)
        index += 1

    # 6.4 添加坏蛋
    # 6.4.1 show the badguys
    # 将坏蛋列表的坏蛋显示到屏幕
    for badguy in badguys:
        screen.blit(badguyimg,badguy)
    # 6.4.2 next badguy
    # 定时结束，添加坏蛋到坏蛋列表
    if badtimer == 0:
        badguys.append([640,random.randint(50,430)])
        badtimer = 100-(badtimer1*2)
            # 定时器设置：先慢后快
        if badtimer1>=35:
            badtimer = 35
        else:
            badtimer1 += 5
    # 6.4.3 attack castle
    index = 0
    for badguy in badguys:
        # 坏蛋以速度7，向前行进
        badguy[0] -= 7
        # 炸碉堡的坏蛋被删除，碉堡掉健康值
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left<64:
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        # check for collisions
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                # 检测两个对象是否重叠
                enemy.play()
                acc[0] += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        index += 1

    # 6.5 添加血槽
    screen.blit(healthbar,(5,5))
        # 先画一个全红色的生命值条
    for health1 in range(healthvalue):
        screen.blit(health,(health1+8,8))
        # 根据承包的生命值往生命条里添加绿色

    # 7、update the screen
    # 7 - 更新屏幕

    # 添加一个计时器：游戏90秒倒计时
    font = pygame.font.Font(None,24)
    survivedtext = font.render(str(int((90000-pygame.time.get_ticks())/60000)).zfill(2)
                               +":"+str(int((90000-pygame.time.get_ticks())/1000%60)).zfill(2),
                               True,(0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635,5]
    screen.blit(survivedtext,textRect)

    #　更新屏幕显示
    pygame.display.flip()

    # 8、loop through the ecents
    # 8 - 检查一些新的事件，如果有退出命令，则终止程序的运行
    # pygame里,用给按键添加事件的方法，来检测按键。

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # check if event is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            # check if event is the X button,it is for moving
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 鼠标如果被点击，得到鼠标位置并计算箭头旋转角度
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])

    # 9、move player
    if keys[0]:
        playerpos[1]-=10
    elif keys[2]:
        playerpos[1]+=10
    elif keys[1]:
        playerpos[0]-=10
    elif keys[3]:
        playerpos[0]+=10

    # 10、Win/Lose check
    if pygame.time.get_ticks()>=90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = format(acc[0]/acc[1]*100,'.2f')
    else:
        accuracy = 0

# 11、Win/Lose display
# 显示胜负图片
if running == 0 and exitcode == 0:
    screen.blit(gameover,(0,0))
else:
    screen.blit(youwin,(0,0))
# 显示胜率
pygame.font.init()
font = pygame.font.Font(None,24)
text = font.render("Accuracy:"+str(accuracy)+"%",True,(255,0,0))
textRect = text.get_rect()
textRect.topright = [350,250]
screen.blit(text,textRect)
# 刷新
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
    pygame.mixer.music.stop()