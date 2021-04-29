import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
#监视键盘鼠标事件
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):

    for event in pygame.event.get():
        # 退出监听
        if event.type==pygame.QUIT:
            sys.exit()
        #左右移动监听
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens,
                    bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats,sb,play_button, ship, aliens,
                    bullets, mouse_x, mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active=True
        #重置记分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空外星人子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event,ai_settings,screen,ship,bullets):
    #按下响应
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)


def check_keyup_events(event,ship):
    #松开响应
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False
    elif event.key == pygame.K_q:
        sys.exit()

#更新子弹，删除消失子弹
def update_bullets(ai_settings, screen,stats,sb,ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,
                                  ship,aliens,bullets)

#检查是否击中外星人，更新外星人
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,
                                  ship,aliens,bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens)==0:
        #删除现有子弹，并创建新的外星人
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)
#检查是否诞生新的最高分
def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
#发射子弹
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建新的子弹，添加到group
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


#外星人部分
#计算一行容纳几个
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

#计算能容纳几列
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=(ai_settings.screen_height-(3 * alien_height) - ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

#创建外外星人
def create_fleet(ai_settings,screen,ship,aliens):
    #创建一个外星人计算可容纳多少外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
#更新外星人
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    #将ship减1
    if stats.ships_left>1:
        stats.ships_left-=1
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新外星人，将飞船放到屏幕低端
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

#
def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
    #检查是否有外星人到达屏幕底端
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            #重新开始游戏
            ship_hit(ai_settings, stats, screen,sb, ship, aliens, bullets)
            break

#改变移动方向
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1
#刷新后重新绘制
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #显示积分板
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()