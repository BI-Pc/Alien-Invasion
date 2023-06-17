import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

# 为了让游戏的循环运行，我们需要不断地检查有没有发生某个事件，
# 比如按键或者松开，而对这些事件都要做出相应的响应，比如移动飞船
# 为了让程序能够响应事件，我们编写一个名为check_events()的函数
# 这个函数将包含我们在游戏运行时检查的事件


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    # 创建一个Settings实例
    game_settings = Settings()
    # 创建一个名为screen的显示窗口，引用pygame.display.set_mode()，这个方法接受一个元组，指定游戏窗口的尺寸
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height)
    )

    # 设置窗口的标题
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(game_settings, screen, "Play")
    # 引用Ship类，创建一个Ship实例，并将其存储在变量ship中
    ship = Ship(game_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个外星人编组
    aliens = Group()
    # 创建一个外星人群
    game_functions.create_fleet(game_settings, screen, ship, aliens)
    # 创建一个用于统计游戏信息的实例
    stats = GameStats(game_settings)
    # 创建记分牌
    scoreboard = Scoreboard(game_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        game_functions.check_events(
            game_settings, ship, screen, bullets, stats, play_button, aliens, scoreboard
        )
        if stats.game_active:
            # 更新飞船的位置（可以直接调用Ship类中的update方法，因为ship是一个实例）
            ship.update()
            # 更新子弹的位置（不能直接调用Bullet类中的update方法，因为bullets是一个编组）
            game_functions.update_bullets(
                game_settings, screen, ship, bullets, aliens, stats, scoreboard
            )
            # 更新外星人的位置
            game_functions.update_aliens(
                game_settings, stats, screen, ship, aliens, bullets, scoreboard
            )

        # 每次循环时都重绘屏幕，包含背景色和飞船和子弹
        game_functions.draw_screen(
            game_settings, stats, screen, ship, bullets, aliens, play_button, scoreboard
        )


run_game()
