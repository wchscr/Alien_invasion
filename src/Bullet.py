import pygame
#“精灵”类
from pygame.sprite import Sprite

class Bullet(Sprite):   #Bullet作为子类继承父类Sprite
    #对飞船发射的子弹进行群组式的管理

    def __init__(self, ai_settings, screen, ship):
        """
        在飞船所在的位置创建一个子弹对象
        :param ai_settings: 游戏设置对象
        :param screen: 屏幕对象
        :param ship: 飞船对象
        """
        super().__init__() # 调用父类Sprite的构造函数
        self.screen = screen

        #在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)   #现在（0，0）处创建子弹
        self.rect.centerx = ship.rect.centerx   #将子弹移动到飞船处
        self.rect.top = ship.rect.top           #将子弹移动到飞船头部

        #存储用小数表示的子弹纵轴位置
        self.y = float(self.rect.y)

        #设置子弹的颜色和飞行速度
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        # 超级子弹


    def update(self):
        #向上移动子弹
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        #在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)

