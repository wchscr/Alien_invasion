import pygame
from Settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_height, ai_settings.screen_height))   #设置游戏窗口大小
    pygame.display.set_caption("打外星人")  #游戏名

    # 初始化背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load('bgm/bgm.mp3')
    pygame.mixer.music.play(-1, 0.0)

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    super_bullets = Group() # 超级子弹
    #创建一个外星人编组
    aliens = Group()
    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #创建外星人人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #游戏主循环
    while True:
        #检查事件的发生
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, super_bullets)
        if stats.game_active:
            # 如果飞船还活着才更新实体状态
            ship.update() # 更新飞船状态
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, super_bullets) # 更新子弹状态
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, super_bullets) # 更新外星人状态
        # 每次循环都重绘屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, super_bullets, play_button)

if __name__ == '__main__':
    run_game() #启动游戏