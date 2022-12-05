
class Settings():
    def __init__(self, player_laser_cooldown):
        self.player_laser_cooldown = player_laser_cooldown

    def increase_speed(self):
        print('decreasing speed')
        self.player_laser_cooldown /=10
        print(self.player_laser_cooldown)
