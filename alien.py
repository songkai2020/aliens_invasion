import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        super(Alien,self).__init__()
        self.ai_settings=ai_settings
        self.screen=screen

        #加载图像,设置rect属性
        self.image=pygame.image.load(r'images/alien.bmp')
        self.rect=self.image.get_rect()

        #每个外星人初始在左上角
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        #存储外新人准确位置
        self.x=float(self.rect.x)
    def update(self):
        self.x+=(self.ai_settings.alien_speed_factor*
                self.ai_settings.fleet_direction)
        self.rect.x=self.x

    def check_edges(self):
        #如果外星人位于屏幕边缘返回True
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True

    def blitem(self):
        self.screen.blit(self.image,self.rect)