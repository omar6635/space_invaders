# Importing the modules
import pygame
import sys
import random
import pygame_menu


class Settings:
    """
    Making the speed, alien quantity and window size of the game variable. The start menu of the game and it's
    interaction is created using the game_menu method. Made by Michael.
    """
    def __init__(self):
        self.game_speed = 100
        self.alien_quantity = 30
        self.__window_size = [1000, 1000]
        self.screen = pygame.display.set_mode(self.__window_size)

    @property
    def window_size(self):
        return self.__window_size

    @window_size.setter
    def window_size(self, value):
        self.__window_size = value

    def game_menu(self):

        def set_difficulty(alien_amount, value):  # alien_amount is needed because of menu.add.selector
            self.alien_quantity = value

        def start_the_game():
            menu.disable()

        menu = pygame_menu.Menu('Space Invaders', self.__window_size[0], self.__window_size[1],
                                theme=pygame_menu.themes.THEME_DARK,)

        menu.add.selector('Aliens :', [('10', 10), ('20', 20), ('30', 30), ('50', 50)], onchange=set_difficulty)
        menu.add.button('Play', start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)


class Ship(pygame.sprite.Sprite):
    """
    inherits from the class sprite. The class defines the dimensions of a ship and processes all keys pressed during
    the game. Made by Michael and Omar.
    """
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.scaled_image = pygame.transform.scale(pygame.image.load(
            "./Grafiken_SpaceInvaders/space_invaders_ship.png")
                                                   , (60, 50))
        self.rect = self.scaled_image.get_rect()
        self.rect.x = settings.window_size[0] // 2
        self.rect.y = settings.window_size[1] * 0.85 // 1
        self.firing_allowed = True
        self.lives = 3

    def handle_keys(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            if key_pressed[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif key_pressed[pygame.K_LEFT] and self.rect.x > 0:
                self.rect.x -= 6
            elif key_pressed[pygame.K_RIGHT] and self.rect.x < (self.settings.window_size[0] - 50):
                self.rect.x += 6
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and self.firing_allowed:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    self.firing_allowed = False


class Shield(pygame.sprite.Sprite):
    """
    Inherits from the sprite class. Defines the deminsions, interaction and image of the barriers. Made by Michael and
    Omar.
    """
    def __init__(self, settings, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.current_frame = 0
        self.image = pygame.image.load(f"./Grafiken_SpaceInvaders/ShieldStates/ShieldHit_{self.current_frame}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def block_oncoming(self, shield_group, laser):
        """
        Responsible for cycling through the different states of the barrier if laser collision took place. Also returns
        a bool depending on laser collision.
        :param shield_group: The group of shields
        :param laser: the laser of the ship
        :return: boolean
        """
        for shield in shield_group:
            if shield.rect.colliderect(laser.rect):
                if shield.current_frame == 2:
                    shield_group.remove(shield)
                    return True
                shield.current_frame += 1
                shield.image = pygame.image.load(f"./Grafiken_SpaceInvaders/ShieldStates/ShieldHit_{shield.current_frame}.png")
                return True
        return False

    def spawn_shield_group(self):
        """
        spawns the shield group in front of the ship.
        :return: group of shields
        """
        shield_group = pygame.sprite.Group()
        space_multiplier_for_shield = 0.15
        for AddShield in range(4):
            shield_to_add = Shield(self.settings, self.settings.window_size[0] * space_multiplier_for_shield // 1,
                                   self.settings.window_size[1] * 0.7 // 1)
            shield_group.add(shield_to_add)
            space_multiplier_for_shield += 0.2
        return shield_group


class Alien(pygame.sprite.Sprite):
    """
    Inherits from the class sprite. Defines the deminsions, interaction and image of the barriers. Made by Omar.
    """
    def __init__(self, x, y, settings, image, alien_id: int):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = 1
        self.row_to_move = -1
        self.alien_next_frame_counter = 0
        self.alien_frame = 1
        self.id = alien_id

    def update_pos(self, alien_group):
        """
        Update the pos of every alien in the group. If they touch one of the edges, the alien rows are moved one down
        starting from the bottommost row.
        :param alien_group: group of aliens
        :return: None
        """
        list_of_sprites_in_group = pygame.sprite.Group.sprites(alien_group)
        list_of_sprites_2d = self.convert_group_list_to_2d(list_of_sprites_in_group)
        for sprites_for_detection in list_of_sprites_in_group:

            if sprites_for_detection.rect.x >= 940:
                self.direction = -1
            elif sprites_for_detection.rect.x <= 0:
                self.direction = 1
            if sprites_for_detection.rect.x >= 940 or sprites_for_detection.rect.x <= 0:
                for sprites in list_of_sprites_2d[len(list_of_sprites_2d) + self.row_to_move]:
                    sprites.rect.move_ip(0, 10)
                self.row_to_move -= 1
                if (self.row_to_move*-1) == len(list_of_sprites_2d)+1:
                    self.row_to_move = -1
                    break

            if sprites_for_detection.rect.y > 800:
                main()

        if self.row_to_move == -1:
            for alien_element in alien_group:
                alien_element.rect.move_ip(self.direction, 0)

    def convert_group_list_to_2d(self, group_list):
        """
        Convert the list of sprites from the group two a two dimensional list for processing purposes for the
        update_pos method.
        :param group_list: list of sprites of a group derived using pygame.sprite.Group.sprites(group).
        :return: two dimensional list
        """
        zwei_dimensional_liste_mit_den_sprites = []
        puffer_list = []

        for elements in group_list:
            puffer_list.append(elements)
            if len(puffer_list) == 9:
                zwei_dimensional_liste_mit_den_sprites.append(puffer_list)
                puffer_list = []

        if len(puffer_list) != 0:
            zwei_dimensional_liste_mit_den_sprites.append(puffer_list)
        return zwei_dimensional_liste_mit_den_sprites

    def choose_random_alien_to_shoot(self, alien_group):
        """
        pick a random alien to shoot a bullet.
        :param alien_group: group of aliens.
        :return: the rect.center of the alien that's been randomly selected.
        """
        alien_to_shoot = random.choice(pygame.sprite.Group.sprites(alien_group))
        return alien_to_shoot.rect.center

    def create_alien_group(self):
        """
        create the group of aliens. The sprites of the aliens are overwritten in another method so they aren't defined
        here.
        :return: group of aliens
        """
        alien_group = pygame.sprite.Group()
        draw_y = 0.2
        draw_x = 0.25

        for alien in range(self.settings.alien_quantity):
            if self.id % 10 == 0 and self.id != 0:
                draw_y += 0.05
                draw_x = 0.05
                if draw_y > 0.14:
                    draw_x = 0.245

            alien_obj = Alien(self.settings.window_size[0] * draw_x, self.settings.window_size[1] * draw_y,
                              self.settings, f"./Grafiken_SpaceInvaders/alien_type_0_frame_2.png", self.id)
            alien_group.add(alien_obj)
            draw_x += 0.05
            self.id += 1
        return alien_group

    def animate_aliens(self, alien_group, alien_init):
        """
        Choose the next image of the alien to give the effect of movement. The sprites of the aliens are defined here.
        The self.id attribute is used to distinguish between the different aliens and assign them the appropriate image.
        :param alien_group: group of aliens
        :param alien_init: alien_init variable defined in main()
        :return: None
        """
        alien_counter = 0
        if alien_init.alien_next_frame_counter > 10:
            if alien_init.alien_frame == 1:
                alien_init.alien_frame += 1
            else:
                alien_init.alien_frame -= 1
            alien_init.alien_next_frame_counter = 0
        for alien in alien_group:
            if alien.id <= 9:
                alien.image = pygame.transform.scale(
                    pygame.image.load(f"./Grafiken_SpaceInvaders/alien_type_0_frame_{alien_init.alien_frame}.png"),
                    (40, 40))
            if 29 >= alien.id > 9:
                alien.image = pygame.transform.scale(
                    pygame.image.load(f"./Grafiken_SpaceInvaders/alien_type_1_frame_{alien_init.alien_frame}.png"),
                    (50, 40))
            if alien.id > 29:
                alien.image = pygame.transform.scale(
                    pygame.image.load(f"./Grafiken_SpaceInvaders/alien_type_2_frame_{alien_init.alien_frame}.png"),
                    (50, 40))
            alien_counter += 1
        alien_init.alien_next_frame_counter += 1


class Score:
    """
    Made by Michael and Omar.
    """
    def __init__(self):
        self.value = 0

    def collision_detection_and_update_score(self, laser, alien_group):
        """
        Checks collision between the laser and an alien from the alien group. Every enemy killed equals 10 points.
        :param laser: laser of the ship
        :param alien_group: group of aliens
        :return: Boolean
        """
        for alien in alien_group:
            if pygame.sprite.collide_rect(laser, alien):
                alien_group.remove(alien)
                self.value += 10
                return True


class Highscore:
    """
    Made by Omar and Michael.
    """
    def __init__(self):
        self.value = self.define_highscore()

    def define_highscore(self):
        """
        Derive the highscore from an external fille called score.dat. If the file is not available, return zero.
        :return: integer
        """
        try:
            file = open("score.txt", "r")
            value_str = file.read()
            file.close()
            return int(value_str)
        except FileNotFoundError:
            return 0

    def update_highscore(self, score):
        """
        update the highscore if score is higher than it.
        :return: None
        """
        if score > self.value:
            self.value = score

    def save_highscore_in_external_file(self):
        """
        write the highscore in an external file.
        :return: None
        """
        file = open("score.txt", "w")
        file.write(str(self.value))
        file.close()


class Laser(pygame.sprite.Sprite):
    """
    Inherits from the class sprite. Defines the deminsions and image of the laser. This class is also used for the
    bullet, with some attributes being overwritten. Made by Michael.
    """
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.ship = ship
        self.image = pygame.transform.scale(pygame.image.load("./Grafiken_SpaceInvaders/laser.PNG"), (15, 25))
        self.rect = self.image.get_rect()
        self.rect.x = self.ship.rect.x + 23
        self.rect.y = 866


class Game:
    """
    Class for interaction between the other classes. Made by Michael and Omar.
    """
    def __init__(self, settings):
        self.settings = settings
        self.ship = Ship(settings)
        self.shield = Shield(settings, 0, 0)
        self.alien = Alien(0, 0, self.settings, "./Grafiken_SpaceInvaders/alien_type_1_frame_1.png", 0)
        self.bullet = True
        self.laser = False

    def detect_laser_collision(self, shield_group, laser_obj, alien_group, ship, score):
        """
        detect ship laser collision with other objects and reposition the laser in the case of a collision.
        :param shield_group: group of shields
        :param laser_obj: laser of ship
        :param alien_group: group of aliens
        :param ship: the ship
        :param score: the score
        :return: None
        """
        if laser_obj.rect.y == 866:
            laser_obj.rect.x = ship.rect.x + 23
        if not ship.firing_allowed:
            laser_obj.rect.move_ip(0, -13)
            if laser_obj.rect.y < -50 or self.shield.block_oncoming(shield_group, laser_obj) or \
                    score.collision_detection_and_update_score(laser_obj, alien_group):
                ship.firing_allowed = True
                laser_obj.rect.x = ship.rect.x + 23
                laser_obj.rect.y = 866

    def detect_bullet_collision(self, bullet_obj, ship_obj, shield_group, alien_group, highscore):
        """
        detect enemy bullet collision with other objects and reposition the bullet in the case of a collision.
        :param bullet_obj: the bullet of the enemy
        :param ship_obj: the ship
        :param shield_group: group of shields
        :param alien_group: group of enemies
        :return: None
        """
        bullet_obj.rect.move_ip(0, 20)
        if bullet_obj.rect.colliderect(ship_obj.rect):
            ship_obj.lives -= 1
            if ship_obj.lives == 0:
                highscore.save_highscore_in_external_file()
                main()
        if len(alien_group) == 0:
            main()
        if self.shield.block_oncoming(shield_group, bullet_obj) or bullet_obj.rect.y > 1000 or \
                bullet_obj.rect.colliderect(ship_obj.rect):
            self.bullet = True
            bullet_obj.rect[0:2] = self.alien.choose_random_alien_to_shoot(alien_group)

    def make_alien_fire_bullet(self, alien_group):
        """
        Spawn a bullet at the middle rect of a randomly selected alien.
        :param alien_group: group of aliens
        :return: Laser object or boolean
        """
        if self.bullet:
            bullet = Laser(self.ship)
            bullet.rect[0:2] = self.alien.choose_random_alien_to_shoot(alien_group)
            self.bullet = False
            bullet.image = pygame.transform.scale(pygame.image.load("./Grafiken_SpaceInvaders/bullet.png"), (30, 20))
            return bullet
        return False

    def make_ship_laser(self, ship):
        """
        spawn the ship laser
        :param ship: the ship
        :return: laser object
        """
        laser = Laser(ship)
        return laser


def main():
    """
    Main Program, where pygame is initialized and the game logic is put together using the classes,
    methods and attributes. Made by Michael and Omar.
    """
    # Initializing pygame and defining the clock for fps and the background
    pygame.init()
    clock = pygame.time.Clock()
    bg = pygame.image.load("./Grafiken_SpaceInvaders/BackgroundPhoto.jpg")
    # Game settings and screen size (the value of window_size can be changed as it is has a getter and setter)
    settings = Settings()
    screen = pygame.display.set_mode(settings.window_size)
    # Defining all the objects and groups that are used in the game and also calling the menu method for the game menu
    settings.game_menu()
    game_init = Game(settings)
    ship = Ship(settings)
    score = Score()
    highscore = Highscore()
    alien_init = Alien(settings.window_size[0]//2,
                       settings.window_size[1]//2, settings, "./Grafiken_SpaceInvaders/alien_type_1_frame_1.png", 0)
    shield_object = Shield(settings, 0, 0)
    shield_group = shield_object.spawn_shield_group()
    laser = game_init.make_ship_laser(ship)
    alien_group = alien_init.create_alien_group()
    bullet = game_init.make_alien_fire_bullet(alien_group)
    # Font for score and lives at the upper left. Made using pygame.font.SysFont(filename, size).
    myfont = pygame.font.SysFont("monospace", 16)
    # The infinite loop for the game
    while True:
        # Keyboard inputs are interpreted and processed with handle keys
        ship.handle_keys()
        # Making the aliens move to the right or the left
        alien_init.update_pos(alien_group)
        # Detect if the bullet or laser has collided with a barrier or other object and execute the appropriate action
        game_init.detect_bullet_collision(bullet, ship, shield_group, alien_group, highscore)
        game_init.detect_laser_collision(shield_group, laser, alien_group, ship, score)
        # Update all aliens to the next sprite to give the effect that they are alive
        alien_init.animate_aliens(alien_group, alien_init)
        # Update highscore
        highscore.update_highscore(score.value)
        # Render lives, score and highscore using the pygame.font.Font.render function
        score_text = myfont.render(f"SCORE: {score.value} ", False, (255, 255, 255))
        actual_score = myfont.render(f"HIGH-SCORE: {highscore.value}", False, (255, 255, 255))
        lives = myfont.render(f"LIVES: {ship.lives*'♥'}", False, (255, 255, 255))
        # Draw all the sprites and groups on the screen and the scores and lives
        screen.blit(bg, (0, 0))
        shield_group.draw(screen)
        alien_group.draw(screen)
        screen.blit(laser.image, laser.rect)
        screen.blit(ship.scaled_image, ship.rect)
        screen.blit(bullet.image, bullet.rect)
        screen.blit(score_text, (5, 10))
        screen.blit(actual_score, (5, 30))
        screen.blit(lives, (5, 50))
        # Everything on the game field is updated
        pygame.display.update()
        # The speed of the game is defined using the previously defined clock variable
        clock.tick(settings.game_speed)


# Call main
main()
