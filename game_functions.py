import pygame
import sys
from bullet import Bullet
from alien import Alien

def check_events(bullet_settings,ship,screen,bullets):
    """响应按键和鼠标事件，用于主程序中的while循环"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event,bullet_settings,ship,screen,bullets)
        elif event.type == pygame.KEYUP:
            check_up_events(event,ship)

def check_down_events(event,bullet_settings,ship,screen,bullets):
    """检测按键方向键事件，用于主程序中的while循环"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # 按下左箭头键，飞船向左移动
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 按下上箭头键，飞船向上移动
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    # 按下下箭头键，飞船向下移动
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    # 按下空格键，创建一颗子弹，并将其加入到编组bullets中
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullet_settings,screen,ship,bullets)
    # 按下ESC键，退出游戏
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_up_events(event,ship):
    """检测按键方向键事件，用于主程序中的while循环"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # 松开左箭头键，飞船停止向左移动
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # 松开上箭头键，飞船停止向上移动
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    # 松开下箭头键，飞船停止向下移动
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def fire_bullet(bullet_settings,screen,ship,bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 如果子弹的数量小于设置的限制，就创建一颗子弹
    if len(bullets) < bullet_settings.bullet_allowed:
        new_bullet = Bullet(bullet_settings,screen,ship)
        # 将新创建的子弹加入到编组bullets中
        bullets.add(new_bullet)

def update_bullets(bullets):
    """更新子弹的位置，并删除已消失的子弹，
    因为主程序中创建的子弹编组，子弹实例在fire_bullet()中创建并加入到编组中，
    所以Bullet类的update方法在这里调用"""
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹,这里使用了副本，因为不能在循环中删除列表元素
    # 会导致循环出错
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def get_aliens_number_x(screen_settings,alien_width):
    """计算一行可以容纳多少个外星人"""
    available_space_x = screen_settings.screen_width - 2 * alien_width
    aliens_number_x = int(available_space_x / (2 * alien_width))
    return aliens_number_x

def create_alien(alien_settings,screen,aliens,alien_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(alien_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(alien_settings,screen_settings,screen,aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳多少个外星人
    # 外星人的间距为外星人的宽度,外星人的间距为外星人的高度
    alien = Alien(alien_settings,screen)
    aliens_number_x = get_aliens_number_x(screen_settings,alien.rect.width)

    # 创建第一行外星人
    for alien_number in range(aliens_number_x):
        # 创建一个外星人并将其加入到当前行
        create_alien(screen_settings,screen,aliens,alien_number)

def draw_screen(screen_settings,screen,ship,bullets,aliens):
    """更新屏幕上的图像，并切换到新屏幕，用于主程序中的while循环"""
    # 用背景色填充屏幕
    screen.fill(screen_settings.bg_color)
    # 在屏幕的指定位置绘制飞船
    ship.blit_ship()
    # 在屏幕的指定位置绘制外星人
    aliens.draw(screen)
    # 在屏幕的指定位置绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
