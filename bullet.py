import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    def __init__(self,bullet_settings,screen,ship):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen
        # 在（0,0）处创建一个表示子弹的矩形，再设置正确的位置
        # 创建子弹的属性rect时，使用了pygame.Rect()类从而能够使用矩形对象的属性和方法
        # 创建子弹的rect时，先创建了一个表示子弹的矩形，再根据飞船的rect属性来设置子弹的初始位置
        # 这样子弹就是从飞船顶部射出的
        self.rect = pygame.Rect(0,0,bullet_settings.bullet_width,bullet_settings.bullet_height)
        self.rect.centerx = ship.ship_rect.centerx
        self.rect.top = ship.ship_rect.top
        # 存储用小数表示的子弹位置
        self.bullet_y = float(self.rect.y)
        self.bullet_color = bullet_settings.bullet_color
        self.bullet_speed_factor = bullet_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.bullet_y -= self.bullet_speed_factor

        # 更新表示子弹的rect的位置
        self.rect.y = self.bullet_y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.bullet_color,self.rect)