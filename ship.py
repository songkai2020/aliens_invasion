import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        #初始化飞船并设置初始位置
        self.screen=screen
        self.ai_settings=ai_settings
        #加载飞船图像,并获取外接矩形
        self.image=pygame.image.load(r'images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom

        self.move_right=False
        self.move_left=False
        #飞船的center属性存储小数
        self.center=float(self.rect.centerx)

    def center_ship(self):
        self.center=self.screen_rect.centerx

    def blitme(self):
        #指定位置绘制飞船
        self.screen.blit(self.image,self.rect)
    def update(self):
        #控制飞船活动范围
        if self.move_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left >0:
            self.center-=self.ai_settings.ship_speed_factor
        #将飞船位置设置为更新后的结果（浮点数类型）
        self.rect.centerx=self.center