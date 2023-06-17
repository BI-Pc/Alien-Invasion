import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, game_settings, screen):
        """初始化飞船并设置其初始位置，用于主程序中"""
        super().__init__()
        # screen在主程序中创建，然后传递给Ship类（主程序第19行）
        self.screen = screen
        # game_settings在主程序中创建，然后传递给Ship类（主程序第17行）
        self.game_settings = game_settings
        # 加载飞船图像并缩放大小
        self.image = pygame.image.load("images/ship.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        # 使用get_rect()获取飞船的矩形属性
        self.rect = self.image.get_rect()
        # 使用get_rect()获取屏幕的矩形属性
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        # 将飞船的矩形属性centerx设置为屏幕矩形的属性centerx的值
        self.rect.centerx = self.screen_rect.centerx
        # 将飞船的矩形属性bottom设置为表示屏幕的矩形的属性bottom的值
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center和bottom中存储小数值，float()将值转换为小数,
        # 这样就可以设置飞船的速度为浮点小数
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置，用于主程序中的while循环"""
        # 用四个独立的if语句，而不是elif语句，以保证玩家同时按下左右箭头键时，飞船不会向右移动
        # 飞船移动范围限制在屏幕内
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 飞船在初始位置沿X轴递增，向右移动
            self.center += self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # 飞船在初始位置沿X轴递减，向左移动
            self.center -= self.game_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            # 飞船在初始位置沿Y轴递减，向上移动
            self.bottom -= self.game_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            # 飞船在初始位置沿Y轴递增，向下移动
            self.bottom += self.game_settings.ship_speed_factor

        # 更新飞船X轴的center值
        self.rect.centerx = self.center
        # 更新飞船Y轴的bottom值
        self.rect.bottom = self.bottom

    def blit_ship(self):
        """在屏幕的指定位置绘制飞船，用于game_functions.py中的update_screen()函数中"""
        # blit()方法根据self.ship_rect指定的位置将图像绘制到屏幕上
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        # 将飞船的centerx属性设置为表示屏幕的矩形的属性centerx的值
        self.center = self.screen_rect.centerx
        # 将飞船的bottom属性设置为表示屏幕的矩形的属性bottom的值
        self.bottom = self.screen_rect.bottom
