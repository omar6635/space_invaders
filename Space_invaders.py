from abc import ABC
import pygame
import typing
import sys
#  Program is under progress.


class Settings:
    def __init__(self, window_size: tuple, game_speed: int, ship_quantity: int) -> None:
        self.__bg_photo = pygame.image.load("./Grafiken_SpaceInvaders/space_invaders_tank.png")
        self.__game_speed = game_speed
        self.__ship_quantity = ship_quantity
        self.__screen = pygame.display.set_mode(window_size)

    def initialise_pygame(self):
        pygame.init()


class Game(ABC):
    def __init__(self, pos: tuple, sprite) -> None:
        self.__sprite = sprite
        self.__pos = pos
        self.__turn = ""

    def __move(self):
        pass

    def __handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    self.__turn = "Left"
                elif event.key == pygame.K_RIGHT:
                    self.__turn = "Right"


    def __shoot(self):
        pass




class Ship(Game):
    def __init__(self, pos: tuple, sprite) -> None:
        super().__init__(pos, sprite)
        self.__sprite = sprite
        self.__pos = pos

    def __move(self):
        pass

    def __shoot(self):
        pass


class Barrier(Game):
    def __init__(self, pos: tuple, sprite) -> None:
        super().__init__(pos, sprite)
        self.__sprite = sprite
        self.__pos = pos

    def block_oncoming(self):
        pass


class Enemies(Game):
    def __init__(self, pos: tuple, sprite) -> None:
        super().__init__(pos, sprite)
        self.__sprite = sprite
        self.__pos = pos

    def __move(self):
        pass

    def __shoot(self):
        pass
