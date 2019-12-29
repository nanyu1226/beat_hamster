#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/12/16 19:27
# @Author   : Heyangyang
"""
1.游戏三要素  初始化  窗口  事件循环
2.游戏逻辑：
    声音对象：
        属性：进入游戏背景音乐   出土音乐  入土音乐  被击中音乐  锤击音乐
        方法：
            方法1：播放背景音乐
            方法2：播放出土声音
            方法3：播放打中音乐
            方法4：没打中声音
            方法5：进洞声音

    游戏中的，土地及仓鼠洞对象：
        属性：土地背景图片width,height(320,226)  坐标  3个仓鼠洞 （较精确得到仓鼠洞的坐标，固定布标）

    锤子对象：
        属性：举起图片   砸下图片
        方法1：跟踪鼠标
        方法2：姿势切换 并恢复

    仓鼠对象：
        属性：正常进出洞图片  被击中图片
        方法：正常进出洞图片  随机从一个仓鼠洞露出 和隐藏  （一旦被击中，更换成被击中的图片）
"""
import os
import random

import pygame
from pygame.locals import *
from pygame import Rect
import time
from sys import exit


# 创建音乐类
class Music:
    def __init__(self):
        pygame.mixer.music.load(r"beat_hamster/music/start_music.mp3")
        self.hamster_out = pygame.mixer.Sound(r"beat_hamster/music/hamster_out.wav")
        self.hit_sound = pygame.mixer.Sound(r"beat_hamster/music/hit_sound.wav")
        self.hammer_down_miss_sound = pygame.mixer.Sound(r"beat_hamster/music/down&miss_sound.wav")

    # 播放背景音乐
    def display_music(self):
        pygame.mixer.music.play(loops=-1, start=0.0)

    # 播放地鼠出洞
    def hamster_out(self):

        self.hamster_out.play()

    # 播放地鼠被打中
    def hamster_hit(self):

        self.hit_sound.play()

    # 播放锤子放下却没打中地鼠
    def hammer_down_miss(self):
        self.hammer_down_miss_sound.play()

    # 播放进洞声音+
    def hammer_in(self):
        self.hamster_in = pygame.mixer.Sound(r"beat_hamster/music/hamster_in.wav")
        self.hamster_in.play()


# 游戏中的创建背景对象
class Background:
    def __init__(self):
        # 加载背景图片属性
        self.play_background = pygame.image.load(r"beat_hamster/image/background&hole.png")
        self.hammer_in = pygame.image.load(r"beat_hamster/image/Default.png")

    # 播放背景图片
    def display_start_img(self,screen):
        screen.blit(self.play_background,(0,0))


# 创建仓鼠对象
class Hamster(pygame.sprite.Sprite):
    def __init__(self,speed=(0,-1),hamster_out=r'beat_hamster/image/out.png'):
        """
        parameter:note, location is hamster's initial position;other parameters has default values
        """

        pygame.sprite.Sprite.__init__(self)  # 初始化动画精灵
        # 循环初始计数
        self.i = 0
        # 加载地鼠出现的图片
        self.hamster_out = pygame.image.load(hamster_out)  # 图片像素：67*75
        # 添加随机刷新的坐标
        self.location = [(27,120),(125,120),(230,120)]
        # 初始化坐标
        self.position = (27, 120)
        # 以图像的边界为参数，获取矩形边界
        # self.rect = self.hamster_out.get_rect()
        # # 设置矩形区域的初始位置
        # self.rect.left, self.rect.right = location[0],location[1]
        # self.speed = speed


    # 加载仓鼠出现,并且移动(请考虑后续有小窗口的情况下，是否继续使用)
    def hamster_out_blit(self,screen):
        if self.i%15==0:
            self.position = random.choice(self.location)
            self.i = 0
        screen.blit(self.hamster_out,self.position)
        self.i +=1

    # # 创建矩形区域(该区域)，用于让仓鼠逐渐冒出   #　　暂时没用
    # def hamster_move(self):
    #     self.rect.move(self.speed)
    #     if self.rect.top < 0:
    #         self.speed[1] = -self.speed[1]


# 创建surface对象？
"""
surface 对象旋转  angle为正：逆时针旋转  angle为负：顺时针旋转  return surface
pygame.transform.rotate(surface,angle)
"""


# 创建锤子对象
class Hammer:
    def __init__(self):
        # 创建锤子矩形
        self.hammer_up = pygame.image.load(r'beat_hamster/image/up1.png')
        self.hammer_down = pygame.transform.rotate(self.hammer_up, 90)

    # 在鼠标位置显示hammer_up图片
    def blit_hammer_up(self,screen):
        screen.blit(self.hammer_up)

    # 在鼠标位子显示hammer_down图片
    def blit_hammer_down(self,screen):
        screen.blit(self.hammer_down)

    # 逆时针90度旋转锤子并显示
    # def blit_hammer_down(self,screen,x,y):
    #     screen.blit(self.hammer_down,(x,y))

    # 鼠标变成hammer_up
    def mouse_change_to_hammer_up(self,x,y,screen):
        pygame.mouse.set_visible(False)
        x -= 71
        y -= 88.5
        screen.blit(self.hammer_up,(x,y))

    # 鼠标变成hammer_down
    def mouse_change_to_hammer_down(self,x,y,screen):
        pygame.mouse.set_visible(False)
        x -= 71
        y -= 88.5
        screen.blit(self.hammer_down,(x,y))


# 初始化pygame,mixer，创建界面及其标题
class Init:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        # 初始化混音模块
        pygame.mixer.init()
        # 创建屏幕
        self.screen = pygame.display.set_mode((320, 226))
        # 屏幕标题：my_beat_hamster-author:hyy
        pygame.display.set_caption('my_beat_hamster-author:hyy')


# 创建事件循环函数
def envent_loops(music1,screen,clock,mouse_cursor,hammer1,background1,hamster1):

    # 创建事件循环，死循环确保窗口一直显示，处理发生的事件
    loops_envent = True
    while loops_envent:

        # 1秒40次
        clock.tick(40)
        # 获取用户事件
        for event in pygame.event.get():
            # 判断是否是退出事件
            if event.type == pygame.QUIT:
                # 是，则标记位为假，结束循环，并结束游戏
                loops_envent = False
                pygame.quit()
                exit()
            # 判断是否是键盘事件
            if event.type == pygame.KEYDOWN:
                # 则打印该键盘事件
                print(event.key, pygame.K_SPACE)
                # 判断是否是空格按键，
                if event.key == pygame.K_SPACE:
                    # 是空格事件，结束背景音乐播放
                    pygame.mixer.music.stop()
            # 判断是否是鼠标点击事件，如果是，则切换锤子形态，刷新该形态n针
            if event.type == pygame.MOUSEBUTTONDOWN:
                music1.hammer_down_miss_sound.play()
                hammer1.mouse_change_to_hammer_down(x, y, screen)
        # 获取鼠标动态位置
        x, y = pygame.mouse.get_pos()
        # 鼠标变锤子
        hammer1.mouse_change_to_hammer_up(x,y,screen)
        # 获取鼠标按键事件返回一个三元元组（left,mid,right）
        mouse_pressed = pygame.mouse.get_pressed()
        # 刷新仓鼠的位置
        hamster1.hamster_out_blit(screen)
        # 刷新界面，加载新的改动部分
        pygame.display.update()
        # 刷新背景
        background1.display_start_img(screen)


# 主函数
def main():
    # 初始化并创建模块
    init1 = Init()
    screen = init1.screen

    # 创建音乐对象，锤子对象
    music1 = Music()
    # 开启背景音乐播放
    music1.display_music()
    # 创建锤子对象
    hammer1 = Hammer()
    # 创建仓鼠对象
    hamster1 = Hamster()
    # 创建背景对象并加载背景
    background1 = Background()

    # 鼠标转换成锤子  ##################3
    mouse_cursor = pygame.image.load(r'beat_hamster/image/up1.png').convert_alpha()

    # 创建时间控制
    clock = pygame.time.Clock()

    # 创建事件循环
    envent_loops(music1,screen,clock,mouse_cursor,hammer1,background1,hamster1)


if __name__ == '__main__':
    # main()
    os.getcwd()


