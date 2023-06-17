import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(
    game_settings, ship, screen, bullets, stats, play_button, aliens, scoreboard
):
    """响应按键和鼠标事件，用于主程序中的while循环"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, game_settings, ship, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_up_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                stats,
                play_button,
                mouse_x,
                mouse_y,
                aliens,
                game_settings,
                screen,
                ship,
                bullets,
                scoreboard,
            )


def check_down_events(event, game_settings, ship, screen, bullets):
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
        fire_bullet(game_settings, screen, ship, bullets)
    # 按下ESC键，退出游戏
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_up_events(event, ship):
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


def check_play_button(
    stats,
    play_button,
    mouse_x,
    mouse_y,
    aliens,
    game_settings,
    screen,
    ship,
    bullets,
    scoreboard,
):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        game_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(game_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 如果子弹的数量小于设置的限制，就创建一颗子弹
    if len(bullets) < game_settings.bullet_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        # 将新创建的子弹加入到编组bullets中
        bullets.add(new_bullet)


def update_bullets(game_settings, screen, ship, bullets, aliens, stats, scoreboard):
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
    check_bullet_alien_collisions(
        game_settings, screen, ship, bullets, aliens, stats, scoreboard
    )


def check_bullet_alien_collisions(
    game_settings, screen, ship, bullets, aliens, stats, scoreboard
):
    """检测子弹和外星人的碰撞"""
    # 检测子弹和外星人的碰撞
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 外星人被消灭后得分
    if collisions:
        for aliens in collisions.values():
            stats.score = stats.score + game_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    # 如果外星人被消灭完，就重新创建一群外星人
    if len(aliens) == 0:
        bullets.empty()
        game_settings.increase_speed()
        # 提高等级
        stats.level = stats.level + 1
        scoreboard.prep_level()
        create_fleet(game_settings, screen, ship, aliens)


def check_high_score(stats, scoreboard):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def get_aliens_number_x(game_settings, alien_width):
    """计算一行可以容纳多少个外星人"""
    available_space_x = game_settings.screen_width - 2 * alien_width
    aliens_number_x = int(available_space_x / (2 * alien_width))
    return aliens_number_x


def get_aliens_number_y(game_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = game_settings.screen_height - 3 * alien_height - ship_height
    aliens_number_y = int(available_space_y / (2 * alien_height))
    return aliens_number_y


def create_alien(game_settings, screen, aliens, alien_number_x, alien_number_y):
    """创建一个外星人并将其加入到当前行"""
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    # 计算外星人的位置
    alien.x = alien_width + 2 * alien_width * alien_number_x
    alien.y = alien_height + 2 * alien_height * alien_number_y
    # 设置外星人的位置
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    # 将外星人加入到编组aliens中
    aliens.add(alien)


def create_fleet(game_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一外星人
    alien = Alien(game_settings, screen)
    # 计算一行可以容纳多少个外星人
    aliens_number_x = get_aliens_number_x(game_settings, alien.rect.width)
    # 计算屏幕可以容纳多少行外星人
    aliens_number_y = get_aliens_number_y(
        game_settings, ship.rect.height, alien.rect.height
    )

    # 从第一行开始创建外星人
    for alien_number_y in range(aliens_number_y):
        # 从第一列开始创建外星人
        for alien_number_x in range(aliens_number_x):
            # 创建一个外星人并将其加入到当前行
            create_alien(game_settings, screen, aliens, alien_number_x, alien_number_y)


def check_fleet_edges(game_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """将外星人群下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def ship_hit(game_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """响应被外星人撞到的飞船"""
    if stats.ship_left > 0:
        # 将ship_left减1
        stats.ship_left -= 1
        # 更新记分牌
        scoreboard.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        # 游戏结束
        stats.game_active = False
        # 鼠标可见
        pygame.mouse.set_visible(True)


def check_alien_bottom(game_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(game_settings, stats, screen, ship, aliens, bullets, scoreboard)
            break


def update_aliens(game_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, ship, aliens, bullets, scoreboard)

    # 检查是否有外星人到达屏幕底端
    check_alien_bottom(game_settings, stats, screen, ship, aliens, bullets, scoreboard)


def draw_screen(
    game_settings, stats, screen, ship, bullets, aliens, play_button, scoreboard
):
    """更新屏幕上的图像，并切换到新屏幕，用于主程序中的while循环"""
    # 用背景色填充屏幕
    screen.fill(game_settings.bg_color)
    # 在屏幕的指定位置绘制飞船
    ship.blit_ship()
    # 在屏幕的指定位置绘制外星人
    aliens.draw(screen)
    # 在屏幕的指定位置绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制得分
    scoreboard.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
