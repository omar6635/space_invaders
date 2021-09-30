import sys
from abc import ABC
import pygame
#  Program is under progress.


class Settings:
    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.game_speed = 50
        self.ship_quantity = 1
        self.__window_size = (1000, 1000)

    @property
    def window_size(self):
        return self.__window_size

    @window_size.setter
    def window_size(self, value: tuple):
        self.__window_size = value


class Game(ABC):
    def __init__(self, sprite):
        self.sprite = sprite

    def move(self):
        pass


class Ship(Game, Settings, pygame.sprite.Sprite):
    def __init__(self, sprite):
        super(Game, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sprite)
        self.scaled_image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.scaled_image.get_rect()
        self.__pos = [self.window_size[0]//2, self.window_size[1]*0.85//1]
        self.fire_laser = False

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
            elif key_pressed[pygame.K_LEFT]:
                self.__pos[0] -= 3
            elif key_pressed[pygame.K_RIGHT]:
                self.__pos[0] += 3
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and self.fire_laser is False:
                if event.key == pygame.K_SPACE:
                    self.fire_laser = True


class Barrier(Game, Settings):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.__sprite = sprite

    def block_oncoming(self):
        pass

    def position(self):
        pass


class Enemies(Game, Settings):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.__sprite = sprite

    def __move(self):
        pass


class Laser(Ship):
    def __init__(self, sprite, pos):
        Ship.__init__(self, sprite)
        self.sprite = pygame.image.load(sprite).convert()
        self.image = pygame.transform.scale(self.sprite, (5, 20))
        self.rect = self.image.get_rect()
        self.pos_ship = [pos[0]+23, pos[1]]


def main():
    # initialise objects
    pygame.init()
    settings = Settings()
    var = settings.window_size
    screen = pygame.display.set_mode(var)
    clock = pygame.time.Clock()
    tank = Ship("./Grafiken_SpaceInvaders/space_invaders_Tank.png")
    laser_fired = False
    while True:

        screen.fill((0, 0, 0))
        clock.tick(60)
        tank.handle_keys()

        if tank.fire_laser:
            laser = Laser("./Grafiken_SpaceInvaders/shot.png", tank.position)
            tank.fire_laser = False
            laser_fired = True

        if laser_fired:
            laser.pos_ship[1] -= 10
            screen.blit(laser.image, (laser.pos_ship[0], laser.pos_ship[1]))
            if laser.pos_ship[1] == 0:
                laser_fired = False


        screen.blit(tank.scaled_image, (tank.position[0], tank.position [1]))
        pygame.display.flip()


main()

