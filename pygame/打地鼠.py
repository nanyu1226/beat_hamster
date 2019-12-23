#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/12/11 23:04
# @Author   : Heyangyang
import pygame
from pygame.locals import *
from random import randint

# 初始化pygame
pygame.init()

# 屏幕设置
width = 480
height = 360
screen = pygame.display.set_mode((width,height))

# 屏幕标题 “打地鼠-author:hyy”
pygame.display.set_caption("打地鼠_author:hyy")

# 初始化混音器模块
pygame.mixer.init()

# 击中声音加载
HandClap = pygame.mixer.Sound(r'beat_hamster/music/hit.wav')

# 加载背景音乐
pygame.mixer.music.load(r'beat_hamster/music/start_music.mp3')


# loops = -1 ,start = 0  播放背景音乐
pygame.mixer.music.play(-1,0)

# 加载地鼠隐藏的图片
hamster0 = pygame.image.load(r'gou.png')

# 加载地鼠显示的照片
hamster1 = pygame.image.load('gou.png')


# 定义仓鼠类
class Hamster:
    def __init__(self,x,y,w,h,image0,image1):
        self.images = [image0,image1]
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        # 状态，隐藏或显示，image  0表示隐藏
        self.status = randint(0,1)
        # 矩形区属性
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

    # 状态显示方法
    def show(self):
        self.status = 1

    # 状态隐藏方法
    def hide(self):
        self.status = 0

    # 随机在指定位置刷新地鼠状态图片方法
    def draw(self):
        screen.blit(self.images[self.status],(self.x,self.y))

    def collide(self,hammer):
        """
        地鼠和锤子的矩形重叠（打中检测）
        :param hammer:
        :return:地鼠冒出及锤子和地鼠图片有重叠，返回真（碰撞检测）
        """

        return self.rect.colliderect(hammer.rect) and self.status == 1

# 加载锤子的图片
hammer0 = pygame.image.load('gou.png')
hammer1 = pygame.image.load('gou.png')
# 定义锤子类
class Hammer:
    def __init__(self,x,y,w,h,image0,image1):
        self.images = [image0,image1]
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.status = 0  # 表示没敲下的状态

    def setpos(self,x,y):
        self.x = x
        self.y = y
        # 由于锤子跟着鼠标移动，所以它的rect属性要不断重设
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

    # 切换造型
    def posechange(self,no):
        self.status = no

    # 刷新图片位置？？？
    def draw(self):
        screen.blit(self.images[self.status],(self.x,self.y))


# 实例化一个锤子对象
hammer = Hammer(0,0,80,80,hammer0,hammer1)

# 地鼠状态列表？？？
basket = [Hamster(10,10,80,80,hamster0,hamster1),
          Hamster(90,109,80,80,hamster0,hamster1),
          Hamster(290,222,80,80,hamster0,hamster1),
          Hamster(310,59,80,80,hamster0,hamster1),
          Hamster(50,234,80,80,hamster0,hamster1)]

print('显示封面',KEYDOWN)
# 封面图像
surface_image = pygame.image.load(r'beat_hamster/image/Default.png')
out_loop = False

# 创建事件循环
while not out_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            print(event.key,pygame.K_SPACE)
            if event.key == pygame.K_SPACE:
                out_loop = True

        screen.blit(surface_image,(0,0))
        pygame.display.update()
print('进入打地鼠游戏中...')
clock = pygame.time.Clock()
beat = False
# 创建事件循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            beat = True
        if event.type == MOUSEBUTTONUP:
            beat = False

    screen.fill((0,0,0))

    for hamster in basket:
        if randint(0,40) == 0:
            if randint(0,1000)>600:
                hamster.show()
            else:
                hamster.hide()
        hamster.draw()
        if beat == True:
            # 锤子姿态
            hammer.posechange(1)
            # 碰撞检测
            if hamster.collide(hammer):
                hamster.hide()
                # 打中 播放鼓掌音乐
                HandClap.play()
                print('击中')   # 考虑加个计数器，数量达到一定的时候显示Game Over
        else:
            hammer.posechange(0)
    mpos = pygame.mouse.get_pos()
    hammer.setpos(mpos[0],mpos[1])  # 设置到鼠标的位置
    hammer.draw()
    pygame.display.update()
    clock.tick(30)