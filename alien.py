import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self,alien_settings,screen):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = screen
        self.alien_settings = alien_settings
        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.gif')
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 存储外星人的准确位置
        self.alien_x = float(self.rect.x)
        self.alien_y = float(self.rect.y)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        elif self.rect.bottom >= screen_rect.bottom:
            return True
        elif self.rect.top <= 0:
            return True

    def update(self):
        """移动外星人"""
        # 向右移动外星人
        self.alien_x += (self.alien_settings.alien_speed_factor * self.alien_settings.fleet_direction)
        self.rect.x = self.alien_x
        # 向左移动外星人
        self.alien_x -= (self.alien_settings.alien_speed_factor * self.alien_settings.fleet_direction)
        self.rect.x = self.alien_x
        # 向下移动外星人
        self.alien_y += self.alien_settings.fleet_drop_speed
        self.rect.y = self.alien_y
        # 向上移动外星人
        self.alien_y -= self.alien_settings.fleet_drop_speed
        self.rect.y = self.alien_y


    def blit_alien(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)