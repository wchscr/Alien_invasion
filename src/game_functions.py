import pygame
import sys
from  Bullet import Bullet
from Alien import  Alien
from time import sleep
import random

from Super_bullet import superBullet


def check_keydown_events(event,ai_settings, screen, ship, bullets, super_bullets):
    """
    键盘被按下
    :param event: 游戏事件对象
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param ship: 飞船对象
    :param bullets: 子弹编组对象
    :param super_bullets: 超级子弹编组
    """
    if event.key == pygame.K_RIGHT:
        # 飞船向右移动
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 飞船向左移动
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_z:
        # 创建一颗超级子弹，并将其加入到编组bullets中
        fire_super_bullet(ai_settings, screen, ship, super_bullets)
    elif event.key == pygame.K_q:
        #当按下Q键后退出游戏
        sys.exit()

def check_keyup_events(event, ship):
    """
    当键盘被松开
    :param event: 游戏事件对象
    :param ship: 飞船对象
    :return:
    """
    if event.key == pygame.K_RIGHT:
        # 飞船停止向右移动
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # 飞船停止向左移动
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, super_bullets):
    """
    监视键盘和鼠标事件
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 游戏计分牌对象
    :param play_button: 开始游戏按钮对象
    :param ship: 飞船对象
    :param aliens: 外星人编组对象
    :param bullets: 子弹编组对象
    ：:param super_bullets: 超级子弹对象
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: #当键盘被按下
           check_keydown_events(event, ai_settings, screen, ship, bullets, super_bullets)
        elif event.type == pygame.KEYUP:  #当键盘被松开
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, super_bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, super_bullets, mouse_x, mouse_y):
    """
    在玩家点击Play按钮时开始游戏
    :param ai_settings: 游戏设置信息
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param play_button: Play按钮对象
    :param ship: 飞船对象
    :param aliens: 外星人编组对象
    :param bullets: 子弹编组对象
    :param mouse_x: 鼠标位置的x坐标
    :param mouse_y: 鼠标位置的y坐标
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置计分牌图像
        sb.prep_score()       # 准备当前分数
        sb.prep_high_score()  # 准备最高分数
        sb.prep_level()       # 准备当前游戏等级
        sb.prep_ships()       # 准备剩余游戏机会

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        super_bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, super_bullets, play_button):
    """
    更新屏幕上的图像，并切换到新屏幕
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 游戏记分牌对象
    :param ship: 飞船对象
    :param aliens: 外星人编组对象
    :param bullets: 子弹编组对象
    :param super_bullets: 超级子弹编组
    :param play_button: 游戏开始按钮对象
    """
    screen.fill(ai_settings.bg_color)  # 背景颜色

    # 绘制所有的子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制所有超级子弹
    for super_bullet in super_bullets.sprites():
        super_bullet.draw_bullet()

    ship.blitme()  # 飞船
    aliens.draw(screen) #外星人

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就显示Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, super_bullets):
    """
    更新子弹的位置，并删除已消失的子弹
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 记分牌对象
    :param ship: 飞船对象
    :param aliens: 外星人编组对象
    :param bullets: 子弹编组对象
    :param super_bullets: 超级子弹对象
    """

    # 更新子弹的状态
    bullets.update()
    super_bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))

    # 删除已消失的超级子弹
    for super_bullet in super_bullets.copy():
        if super_bullet.rect.bottom <= 0:
            super_bullets.remove(super_bullet)

    # 检查是否有子弹击中了外星人
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, super_bullets)

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, super_bullets):
    """
    检测外星人与飞船相撞
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 游戏记分牌对象
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹编组对象
    :param super_bullets: 超级子弹对象
    """
    # 如果子弹击中了外星人，就删除相应的子弹和外星人
    # 两个布尔类型的实参分别表示是否要删除第一个编组的个体和第二个编组的个体
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    super_collisions = pygame.sprite.groupcollide(super_bullets, aliens, True, True)

    if collisions:
        # 当子弹击中外星人，得分加alien_points
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        # 每次击中外星人后检查最高分是否发送变化
        check_high_score(stats, sb)

    if super_collisions:
        # 当子弹击中外星人，得分加alien_points
        for aliens in super_collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        # 每次击中外星人后检查最高分是否发送变化
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除所有子弹，加快游戏节奏，并创建一群新的外星人
        bullets.empty()
        super_bullets.empty()
        ai_settings.increase_speed()

        # 如果整群外星人都被消灭，就提高一个等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """
    发射新的子弹
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param ship: 飞船对象
    :param bullets: 子弹编组
    """
    if len(bullets) < ai_settings.bullets_allowed:
        # 当子弹数小于允许最大子弹数时才创建新子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def fire_super_bullet(ai_settings, screen, ship, super_bullets):
    """
    发射新的子弹
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param ship: 飞船对象
    :param super_bullets: 子弹编组
    :return:
    """
    if len(super_bullets) < ai_settings.super_bullets_allowed:
        # 当子弹数小于允许最大子弹数时才创建新子弹
        new_bullet = superBullet(ai_settings, screen, ship)
        super_bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """
    计算每行可容纳多少个外星人
    :param ai_settings: 游戏设置
    :param alien_width: 外星人图像的宽度
    :return: 每行可容纳的外星人数量
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """
    计算屏幕可以容纳多少行外星人
    :param ai_settings: 游戏设置
    :param ship_height: 飞船图像长度
    :param alien_height: 外星人图像的长度
    :return: 每次产生多少行外星人
    """
    available_space_y = (ai_settings.screen_width - 3 * alien_height - ship_height)   #给飞船前方流出3行的空白的区域
    number_rows = int(available_space_y / (2 * alien_height))         #每隔一行放置一行外星人
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    创建一个外星人并加入当前行
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param aliens: 外星人编组
    :param alien_number: 当前行外星人的编号
    :param row_number: 当前行的编号
    """
    alien = Alien(ai_settings, screen)
    # 每空一个位置创建一个外星人
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """
    创建外星人人群
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param ship: 飞船对象
    :param aliens: 外星人编组
    """
    #外星人间距为外星人宽度和高度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width) # 计算一行可容纳多少个外星人
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height) # 计算一共可以容纳多少行外星人
    number_rows -= 2  # 调整外星人行数，减2

    # 创建外星人人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            if random.randint(1, 100) /100 < ai_settings.density:
                create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """
    有外星人到达边缘时采取相应的措施
    :param ai_settings: 游戏设置
    :param aliens: 外星人编组
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)   #改变外星人的移动方向
            break

def change_fleet_direction(ai_settings, aliens):
    """
    将外星人整体下移，并改变水平移动方向
    :param ai_settings: 游戏设置
    :param aliens: 外星人编组
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, super_bullets):
    """
    响应被外星人撞到的飞船
    :param ai_settings: 游戏设置
    :param stats: 游戏统计信息对象
    :param screen: 屏幕对象
    :param sb: 记分牌对象
    :param ship: 飞船对象
    :param aliens: 外星人编组
    :param bullets: 子弹编组
    :param super_bullets: 超级子弹编组
    """
    # 将ship_left(剩余命数)减1
    if stats.ship_left > 0:
        stats.ship_left -= 1
        sb.prep_ships() #更新记分牌中，剩余游戏机会
        sleep(0.5)   # 暂停
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True) # 游戏结束时让鼠标可见

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    super_bullets.empty()

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, super_bullets):
    """
    检查是否有外星人到达屏幕底端
    :param ai_settings: 游戏设置
    :param stats: 游戏统计信息对象
    :param screen: 屏幕对象
    :param sb: 记分牌对象
    :param ship: 飞船对象
    :param aliens: 外星人编组
    :param bullets: 子弹编组
    :param super_bullets: 超级子弹编组
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, super_bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, super_bullets):
    """
    检查是否有外星人位于屏幕边缘位置，并更新所有外星人的位置
    :param ai_settings: 游戏设置
    :param stats: 游戏统计信息对象
    :param screen: 屏幕对象
    :param sb: 记分牌对象
    :param ship: 飞船对象
    :param aliens: 外星人编组
    :param bullets: 子弹编组
    :param super_bullets: 超级子弹编组
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    # 方法spritecollideany()接受两个实参：一个“精灵”和一个编组。
    # 它检查编组是否有成员与精灵发生了碰撞，并在找到了与精灵发送碰撞的成员后停止遍历
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, super_bullets)
        # print("飞船没了!")
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, super_bullets)

def check_high_score(stats, sb):
    """
    检查是否诞生了新的最高分
    :param stats: 游戏统计信息对象
    :param sb: 计分板对象
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()