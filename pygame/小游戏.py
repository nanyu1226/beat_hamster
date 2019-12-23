#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/12/11 10:20
# @Author   : Heyangyang

import pygame, sys

'''function: make thing running what you want
   author:chenweihua
   date:2018-11-18
'''

# 初始化
pygame.init()

# 定义游戏窗口尺寸
size = (1000, 800)
width, height = size[0], size[1]

# 运动速度
speed = [1, 1]
# 背景颜色/RGB模式颜色
Black = 231, 222, 1
# 创造一个screen对象
screen = pygame.display.set_mode(size)
# 标题
pygame.display.set_caption("my first game!")
# 引入 小球/对象图片  ps:放到同目录下
ball = pygame.image.load('gou.png')
# 将小球包装成一个矩形对象
ballrect = ball.get_rect()

# 事件逻辑部分
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    ballrect = ballrect.move(speed[0], speed[1])
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    # 窗口更新部分
    screen.fill(Black)
    screen.blit(ball, ballrect)
    pygame.display.update()
