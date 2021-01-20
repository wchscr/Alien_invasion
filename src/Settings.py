class Settings():
    # 存储《外星人入侵》的所有设置类

    def __init__(self):
        #初始化游戏设置

        #游戏窗口大小
        self.screen_width = 800
        self.screen_height = 800
        # 背景颜色
        self.bg_color = (255, 255, 255)

        # 飞船固定属性
        self.ship_limit = 3       # 飞船数量上限

        # 子弹固定属性
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3 #允许的最大子弹数

        # 超级子弹固定属性
        self.super_bullet_width = self.screen_width / 4  #超级子弹的宽度为屏幕宽度的1/4
        self.super_bullet_height = 3
        self.super_bullet_color = (60, 60, 60)
        self.super_bullets_allowed = 1 # 每个关卡允许的超级子弹数

        # 外星人固定属性
        self.fleet_drop_speed = 1      # 外星人垂直移动的速度
        self.density = 0.5             # 外星人生成密度，初始密度50%

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        初始化随游戏进行而变化的设置
        """
        self.ship_speed_factor = 0.8     # 飞船移动速度
        self.bullet_speed_factor = 0.8   # 子弹飞行速度
        self.super_bullet_speed_factor = 0.1 # 超级子弹飞行速度
        self.alien_speed_factor = 0.1  # 外星人水平移动的速度

        # 外星人群的移动方向，1表示向右，-1表示向左
        self.fleet_direction = 1

        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """
        提高速度设置和外星人点数
        """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.density *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
