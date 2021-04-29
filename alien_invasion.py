import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard



def run_game():
    ai_settings=Settings()
    pygame.init()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien_invasion')
    #创建Play按钮
    play_button=Button(ai_settings,screen,'Play')
    stats=GameStats(ai_settings)
    #飞船
    ship=Ship(ai_settings,screen)
    #计分板
    sb=Scoreboard(ai_settings,screen,stats)
    #子弹
    bullets = Group()
    #外星人
    aliens=Group()
    #创建外星人群组函数
    gf.create_fleet(ai_settings,screen,ship,aliens)

    while True:
        #监视键盘鼠标事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen,stats,sb,ship, aliens, bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
            #刷新后重新绘制
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
                         play_button)
        pygame.display.flip()

run_game()