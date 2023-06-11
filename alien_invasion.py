import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions

# 为了让游戏的循环运行，我们需要不断地检查有没有发生某个事件，
# 比如按键或者松开，而对这些事件都要做出相应的响应，比如移动飞船
# 为了让程序能够响应事件，我们编写一个名为check_events()的函数
# 这个函数将包含我们在游戏运行时检查的事件

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    # 虽然都是setting类的实例，但是每个实例都是独立的，可以设置不同的值
    screen_settings = Settings()
    ship_settings = Settings()
    bullet_settings = Settings()
    alien_settings = Settings()
    # 创建一个名为screen的显示窗口，引用pygame.display.set_mode()，这个方法接受一个元组，指定游戏窗口的尺寸
    screen = pygame.display.set_mode((screen_settings.screen_width,screen_settings.screen_height))

    # 设置窗口的标题
    pygame.display.set_caption("Alien Invasion")

    # 引用Ship类，创建一个Ship实例，并将其存储在变量ship中
    ship = Ship(ship_settings,screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个外星人
    alien = Alien(alien_settings,screen)
    # 创建一个外星人编组
    aliens = Group()
    # 创建一个外星人群
    game_functions.create_fleet(alien_settings,screen_settings,screen,aliens)
     
    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        game_functions.check_events(bullet_settings,ship,screen,bullets)
        # 更新飞船的位置（可以直接调用Ship类中的update方法，因为ship是一个实例）
        ship.update()
        # 更新子弹的位置（不能直接调用Bullet类中的update方法，因为bullets是一个编组）
        game_functions.update_bullets(bullets)
        # 每次循环时都重绘屏幕，包含背景色和飞船和子弹
        game_functions.draw_screen(screen_settings,screen,ship,bullets,aliens)

run_game()