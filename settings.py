class Settings():

    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)
        #飞船移动速度
        self.ship_speed_factor=1.5
        self.ship_limit = 3
        #子弹设置
        self.bullet_speed_factor=1
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=60,60,60
        self.bullets_allowed=10

        #外星人水平移动速度
        self.alien_speed_factor=0.5
        #外星人竖直移动速度
        self.fleet_drop_speed=10
        #移动方向1向右，-1向左
        self.fleet_direction=1

        #以什么样的速度加快游戏设置
        self.speedup_scale=1.1
        self.initialize_dynamic_settings()

        #计分
        self.alien_points=50

        #加快速度时相应提高点数
        self.score_scale=1.5

    def initialize_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1

        self.fleet_direction=1

    def increase_speed(self):
        self.ship_speed_factor+=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale

        self.alien_points=int(self.alien_points*self.score_scale)



