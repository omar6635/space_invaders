import sys
from abc import ABC
import pygame


#  Program is under progress.


class Settings:
    def __init__(self):
        self.__bg_color = (0, 0, 0)
        self.__game_speed = 50
        self.__ship_quantity = 1
        self.__window_size = [600, 600]

    @property
    def window_size(self):
        return self.__window_size

    @window_size.setter
    def window_size(self, value: list):
        self.__window_size = value


class Game(ABC):
    def __init__(self, sprite):
        self.__sprite = sprite
        self.__pos = (0, 0)

    def move(self):
        pass


class Ship(Game, Settings, pygame.sprite.Sprite):
    def __init__(self, sprite):
        super(Game, self).__init__()
        super(pygame.sprite.Sprite).__init__()
        self.__image = pygame.image.load(sprite)
        self.__rect = self.__image.get_rect()
        self.__pos = (self.window_size[0]//2, self.window_size[1]*0.2)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    self.__pos[0] -= 3
                elif event.key == pygame.K_RIGHT:
                    self.__pos[0] += 3

    def move(self):
        pass

    def shoot(self):
        pass


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

    def __shoot(self):
        pass


class Laser(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.__sprite = sprite
        self.__shoot = False

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__shoot = not self.__shoot


def main():
    # initialise objects
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    tank = Ship("./Grafiken_SpaceInvaders/space_invaders_tank.png")
    tank_group = pygame.sprite.Group()
    tank_group.add(tank)
    while True:


        pygame.display.update()

        tank_group.draw(screen)
        clock.tick(60)


main()

