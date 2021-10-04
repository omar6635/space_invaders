import sys
from abc import ABC
import pygame
#  Program is under progress.


class Settings:
    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.game_speed = 50
        self.enemy_quantity = 5
        self.__window_size = (1000, 1000)

    @property
    def window_size(self):
        return self.__window_size

    @window_size.setter
    def window_size(self, value: tuple):
        self.__window_size = value


class Game(ABC):
    def __init__(self, sprite):
        self.sprite = pygame.transform.scale(pygame.image.load(sprite), (50, 50))

    def move(self):
        pass


class Ship(Game, Settings, pygame.sprite.Sprite):
    def __init__(self, sprite):
        super(Game, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.scaled_image = pygame.transform.scale(pygame.image.load(sprite), (50, 50))
        self.rect = self.scaled_image.get_rect()
        self.__pos = [self.window_size[0]//2, self.window_size[1]*0.85//1]
        self.fire_laser = False
        self.firing_allowed = True

    @property
    def position(self):
        return self.__pos

    @position.setter
    def position(self, pfirsich):
        self.__pos = pfirsich

    def handle_keys(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed:
            if key_pressed[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif key_pressed[pygame.K_LEFT] and self.__pos[0] > 0:
                self.__pos[0] -= 3
            elif key_pressed[pygame.K_RIGHT] and self.__pos[0] < (self.window_size[0] - 50):
                self.__pos[0] += 3

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and self.firing_allowed:
                if event.key == pygame.K_SPACE:
                    self.fire_laser = True
                    self.firing_allowed = False


class Barrier(Game, Settings):
    def __init__(self, sprite):

        super().__init__(sprite)
        self.__sprite = sprite

    def block_oncoming(self):
        pass

    def position(self):
        pass


class Enemies(Game, Settings, pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        super(Game, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(sprite), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.spawn_locations = [[100, 100], [200, 100], [300, 100], [400, 100], [500, 100]]

    def __move(self):
        pass


class Laser(Ship):
    def __init__(self, sprite, pos):
        Ship.__init__(self, sprite)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite) , (5, 20))
        self.rect = self.sprite.get_rect()
        self.pos_ship = [pos[0]+23, pos[1]]


def main():
    # initialise objects
    pygame.init()
    settings = Settings()
    var = settings.window_size
    screen = pygame.display.set_mode(var)
    clock = pygame.time.Clock()
    tank = Ship("./Grafiken_SpaceInvaders/space_invaders_Tank.png")
    enemy_init = Enemies("./Grafiken_SpaceInvaders/pog.jfif", 0, 0)
    laser_fired = False
    enemy_group = pygame.sprite.Group()

    for enemy in range(settings.enemy_quantity):
        enemy_obj = Enemies("./Grafiken_SpaceInvaders/pog.jfif", enemy_init.spawn_locations[enemy][0], enemy_init.spawn_locations[enemy][1])
        enemy_group.add(enemy_obj)

        """if enemy != 11:
            enemy_obj = Enemies("./Grafiken_SpaceInvaders/enemies.jpg", [settings.window_size[0]*(0.1 * (enemy+1)), settings.window_size[1]*0.1])
        else:
            enemy_obj = Enemies("./Grafiken_SpaceInvaders/enemies.jpg", [settings.window_size[0]*(0.1 * (enemy-10)), settings.window_size[1]*0.2])
        enemy_group.add(enemy_obj)"""

    while True:

        screen.fill((0, 0, 0))

        tank.handle_keys()

        if tank.fire_laser:  # can be simplified or improved
            laser = Laser("./Grafiken_SpaceInvaders/shot.png", tank.position)
            tank.fire_laser = False
            laser_fired = True

        if laser_fired:  # can be simplified or improved
            laser.pos_ship[1] -= 10
            screen.blit(laser.sprite, (laser.pos_ship[0], laser.pos_ship[1]))
            if laser.pos_ship[1] == 0:
                tank.firing_allowed = True

        screen.blit(tank.scaled_image, (tank.position[0], tank.position[1]))
        enemy_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)


main()
