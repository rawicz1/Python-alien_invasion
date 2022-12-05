import pygame, sys
import player
from player import Player
import random
from alien import Alien
from random import randint
from time import sleep
from laser import Laser
import json

screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height)) #((0,0), pygame.FULLSCREEN)

col = random.randint(0, 255)
star_colour = (col, col, col)
velocity1 = 1
velocity2 = 10
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
high_scores_filename = './high_scores/highscores.txt'

class Circle:
    def __init__(self, screen, colour, x, y, size):
        self.screen = screen
        self.colour = colour
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        colour_x = random.randint(100, 255)
        colour1 = (colour_x, colour_x, colour_x)
        self.colour = colour1
        pygame.draw.circle(screen, self.colour, self.x, self.y, self.size)

    def move(self):

            keys = pygame.key.get_pressed()
            tuple_to_list = list(self.x) # to access x value of coordinates tuple
            if tuple_to_list[1] < screen_height:
                tuple_to_list[1] += velocity1
            else:
                tuple_to_list[0] = random.randint(0, screen_width)
                tuple_to_list[1] = 0
            self.x = tuple(tuple_to_list)

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                tuple_to_list = list(self.x)
                if tuple_to_list[1] < screen_height:
                    tuple_to_list[1] += velocity2
                else:
                    tuple_to_list[0] = random.randint(0, screen_width)
                    tuple_to_list[1] = 0
                self.x = tuple(tuple_to_list)

class Circle2(Circle):

    def draw(self):
        colour_x = random.randint(0, 100)
        colour1 = (colour_x, colour_x, colour_x)
        self.colour = colour1
        pygame.draw.circle(screen, self.colour, self.x, self.y, self.size)

    def move(self):
        keys = pygame.key.get_pressed()
        y = list(self.x)
        if y[1] < screen_height:
            y[1] += 1.5
        else:
            y[0] = random.randint(0, screen_width)
            y[1] = 0
        self.x = tuple(y)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y = list(self.x)
            if y[1] < screen_height:
                y[1] += velocity2
            else:
                y[0] = random.randint(0, screen_width)
                y[1] = 0
            self.x = tuple(y)

rectangles = []

for count in range(16):
    colour_x = random.randint(100, 255)
    colour = (colour_x, colour_x, colour_x)
    x = random.randint(0, screen_width)
    y = random.randint(0, 500)
    size = random.randint(0, 2)
    rectangles.append(Circle(screen, colour, (x, y), size, 0))
    colour_x = random.randint(100, 255)
    colour = (colour_x, colour_x, colour_x)
    x = random.randint(0, screen_width)
    y = random.randint(0, 500)
    size = random.randint(0, 2)
    rectangles.append(Circle2(screen, colour, (x, y), size, 0))
#player_laser_cooldown = 500
class Game:
    def __init__(self, fleet_size = 1):
        self.screen = screen
        self.rect = self.screen.get_rect()


        player_sprite = Player((self.screen.get_width()/2, self.screen.get_height()), screen_width, 5)
        self.player_sprite = player_sprite
        self.player = pygame.sprite.GroupSingle(player_sprite)


        self.y = random.randint(0, self.rect.bottom/2)
        alien_sprite = Alien(x, y, self.screen.get_width(), self.player.sprite.rect.top)
        self.alien_sprite = alien_sprite
        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.fleet_size = fleet_size
        self.create_fleet()

        self.level = 1
        self.alien_laser = pygame.sprite.Group()
        self.alien_laser_time = 30
        self.score = 0
        self.top_scores = []
        self.username = ''


    def create_fleet(self):

        for _ in range(self.fleet_size):
            while True:
                screen_rect = self.screen.get_rect()
                player_top_rect = self.player.sprite.rect.top
                x1 = randint(50, screen_width - 50)
                y1 = randint(-200, screen_height // 2)
                new_rect = pygame.Rect(x1, y1, 75, 75)
                if not any(alien1 for alien1 in self.aliens if
                           new_rect.colliderect(alien1.rect.x, alien1.rect.y, 75, 75)):
                    self.aliens.remove()
                    break
            alien_sprite = Alien(x1, y1, screen_rect.right, player_top_rect)
            self.aliens.add(alien_sprite)
            #print(self.player_laser_cooldown)

    def next_level(self):

        if len(self.aliens) == 0:
            text_surface = my_font.render('Next level', False, (255, 0, 0))
            text_rect = text_surface.get_rect()
            screen.blit(text_surface, (self.screen.get_width()/2 - text_rect.width/2, self.screen.get_height()/2 - text_rect.height))
            pygame.display.flip()
            sleep(3)
            self.level += 1
            self.fleet_size += 5
            self.player.empty()
            player.Player.laser_cooldown(self.player_sprite)
            self.player.add(self.player_sprite)
            self.player.update()
            self.alien_laser.empty()
            self.create_fleet()

    def collision_laser_alien(self):

        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    self.score +=100
                    laser.kill()


    def alien_shoot(self):
        sounds = ['./sounds/pio_ship.wav', './sounds/pio1.wav', './sounds/pio2.wav', './sounds/pio3.wav', './sounds/pio4.wav', './sounds/pio5.wav']
        shoot = pygame.mixer.Sound(random.choice(sounds))
        shoot.set_volume(0.1)
        self.alien_laser_time -=1
        if self.alien_laser_time <=0:
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6)
            pygame.mixer.Sound.play(shoot)
            self.alien_laser.add(laser_sprite)
            self.alien_laser_time += 100

    def collision_alien_laser_player(self):

        if self.alien_laser:
            for laser in self.alien_laser:
                if pygame.sprite.spritecollide(laser, self.player, True):
                    self.game_over()


    def alien_bottom_game_over(self):
        for alien3 in self.aliens:
            if alien3.rect.bottom >= self.player.sprite.rect.top:
                #self.aliens.remove(alien3)
                self.game_over()

                #break
                print('test point 2 allien bottom')

    def game_over(self):
        sleep(2)
        screen_y = self.screen.get_height()
        for position in range(screen_y):
            self.screen.fill('black')
            text_surface = my_font.render('Game over!', False, (255, 255, 0))
            text_rect = text_surface.get_rect()
            screen.blit(text_surface, (self.screen.get_width() / 2 - text_rect.width / 2
                                       , screen_y - self.screen.get_height() - text_rect.height))
            sleep(0.001)
            screen_y +=0.5
            pygame.display.flip()

        self.top_scores_list()


    def top_scores_list(self):
        pygame.display.update()
        typing = True
        while True:

            get_input = True
            user_name = ''
            input_rect = pygame.Rect(self.screen.get_width()/2, self.screen.get_height()/2, 250, 100)

            while True:
                for event in pygame.event.get():

                    # if user types QUIT then the screen will close
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_RETURN:
                            self.username = user_name
                            get_input = False




                            self.score_save_to_file()
                            return user_name

                        # Check for backspace
                        elif event.key == pygame.K_BACKSPACE:

                            # get text input from 0 to -1 i.e. end.
                            user_name = user_name[:-1]

                        # Unicode standard is used for string
                        # formation
                        else:
                            user_name += event.unicode
                    get_input = False
                color=255
                text_surface = my_font.render(f"Type in your name: {user_name}", True, (color, color, 0))
                input_rect.center = self.screen.get_width()/2, self.screen.get_height()/2
                pygame.draw.rect(screen, 'black', input_rect)
                screen.blit(text_surface, (input_rect.x , input_rect.y ))
                input_rect.w = max(100, text_surface.get_width() + 10)

                pygame.display.flip()



    def score_save_to_file(self):

        #self.top_scores_list().typing = False

        with open('./high_scores/top_scores.json') as f:
            self.top_scores = json.load(f)

        score = {'score: ':self.score, 'name:': self.username}

        self.top_scores.append(score)
        self.top_scores.sort(key=lambda item: item.get("score: "), reverse=True)
        if len(self.top_scores) >10:
            self.top_scores.pop()
        print(len(self.top_scores))
        filename = 'top_scores.json'
        with open(filename, 'w+') as f:
            json.dump(self.top_scores, f)


        self.score_append_to_list()

    def score_append_to_list(self):

        self.top_scores.clear()
        with open('top_scores.json') as f:
            self.top_scores = json.load(f)
        print(self.top_scores)
        self.screen.fill('black')
        pygame.display.update()
        pygame.display.flip()
        #self.display_top_scores()
        xc = 100
        name_x = 0
        score_x = 0
        for score, name in self.top_scores:
            text_surface = my_font.render(f'{self.top_scores[name_x][name]} - {self.top_scores[score_x][score]}', False, (255, 255, 0))
            text_rect = text_surface.get_rect()
            screen.blit(text_surface, (self.screen.get_width()/2 - text_rect.width/2, xc))
            name_x +=1
            score_x +=1
            xc+=50
            #self.screen.fill('black')
            #pygame.display.flip()
            pygame.display.flip()

        sleep(5)
        pygame.quit()
        sys.exit()
    """def display_top_scores(self):
        #self.screen.fill('black')
        #pygame.display.flip()

        self.screen.fill('black')
        for rectangle in rectangles:
            rectangle.draw()
            rectangle.move()
        pygame.display.flip()"""


        #pygame.quit()
        #sys.exit()


    def display_score(self):

        text_surface = my_font.render(f'Score = {self.score}', False, (0, 255, 0))
        text_rect = text_surface.get_rect()
        screen.blit(text_surface, (10, 10))
        #pygame.display.flip()

    def display_level(self):

        text_surface = my_font.render(f'Level = {self.level}', False, (0, 255, 0))
        text_rect = text_surface.get_rect()
        screen.blit(text_surface, (screen.get_width() - text_surface.get_width()-10, 10))

    def run(self):

        self.player.update()
        self.collision_laser_alien()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        """for alien in self.aliens:
            self.aliens.remove(alien)
            self.aliens.add(alien)"""
        self.alien_shoot()
        self.alien_laser.draw(screen)
        self.alien_laser.update()
        self.aliens.update()
        self.aliens.draw(screen)
        self.next_level()
        self.player.update()
        self.display_score()
        self.display_level()
        self.collision_alien_laser_player()
        #self.top_scores_list()
        self.alien_bottom_game_over()
        for laser in self.alien_laser.copy():
            if laser.rect.bottom >= screen.get_height():
                self.alien_laser.remove(laser)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()))
    clock = pygame.time.Clock()
    game = Game()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')

        for alien in game.aliens:
            game.aliens.remove(alien)
            Alien.alien_collisions(alien, game.aliens)
            game.aliens.add(alien)

        for rectangle in rectangles:
            rectangle.draw()
            rectangle.move()

        game.player.update()

        game.player.sprite.lasers.draw(screen)
        game.player.draw(screen)
        game.run()
        pygame.display.flip()
        clock.tick(60)
