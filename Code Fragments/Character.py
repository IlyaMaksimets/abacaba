import pygame
import mysql.connector

from Bullet import Bullet

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60
G = 0.5

GLOBAL_X = -500

CHARACTER_SPEED = 5

l_1 = pygame.image.load('../Textures/1_lives.png')
l_2 = pygame.image.load('../Textures/2_lives.png')
l_3 = pygame.image.load('../Textures/3_lives.png')
l_4 = pygame.image.load('../Textures/4_lives.png')

CHOSEN_DIFFICULTY = 'beginner'

SONG_VOLUME = 0
SOUNDS_VOLUME = 0

db_connection = mysql.connector.connect(
            host='127.0.0.2',
            user='Tremexen',
            passwd='q4h887dm_RN',
            database='grand_battle-info'
        )

get_info_query1 = "SELECT * FROM `song-volume`"
with db_connection.cursor() as cursor:
    cursor.execute(get_info_query1)
    result1 = cursor.fetchall()
    for (volume_level_id, condition) in result1:
        if condition[:2] == "on":
            SONG_VOLUME += 10

get_info_query2 = "SELECT * FROM `sounds-volume`"
with db_connection.cursor() as cursor:
    cursor.execute(get_info_query2)
    result2 = cursor.fetchall()
    for (volume_level_id, condition) in result2:
        if condition[:2] == "on":
            SONG_VOLUME += 10


def get_new_GLOBAL_X(new_GLOBAL_X):
    requests4 = open('../Other/info-flows/flow_04.txt', 'w')
    requests4.write(str(new_GLOBAL_X))
    requests4.close()


class Character(pygame.sprite.Sprite):

    def __init__(self, x, y, velocity, lives, MAP_MATRIX, screen_scroll1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../Textures/character.png')
        self.flying_gun = pygame.image.load('../Textures/flying_gun.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lives = lives
        self.velocity = velocity
        self.velocity_y = 0
        self.jump = False
        self.air = True
        self.climbing = False
        self.ladder = False
        self.change_direction = False
        self.look_direction = 1
        self.cooldown = 0
        self.check_alive = True
        self.screen_scroll = screen_scroll1

        self.size = self.image.get_size()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.MAP_MATRIX = MAP_MATRIX

        self.actual_buff = 0

    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.image, self.change_direction, False), self.rect)
        if self.look_direction == 1:
            SCREEN.blit(pygame.transform.flip(self.flying_gun, self.change_direction, False),
                        (self.rect.x + self.width * self.look_direction, self.rect.y))
        else:
            SCREEN.blit(pygame.transform.flip(self.flying_gun, self.change_direction, False),
                        (self.rect.x - self.flying_gun.get_width(), self.rect.y))

    def get_x(self):
        return self.rect.x

    def move(self, move_left, move_right):
        global G, GLOBAL_X
        x_change = 0
        y_change = 0
        hit = False
        if move_left:
            x_change = -self.velocity
            self.change_direction = True
            self.look_direction = -1

        if move_right:
            x_change = self.velocity
            self.change_direction = False
            self.look_direction = 1

        if self.jump and self.air is False:
            self.velocity_y = -10
            self.jump = False
            self.air = True

        if not self.ladder:
            self.velocity_y += G
        if self.velocity_y > 12:
            self.velocity_y = 12

        y_change += self.velocity_y
        GLOBAL_X += x_change

        for x in range(len(self.MAP_MATRIX)):
            for y in range(len(self.MAP_MATRIX[x])):
                block = self.MAP_MATRIX[x][y]
                tile = pygame.Rect((240 + y * 50 + self.screen_scroll, x * 50), (50, 50))

                if block == 'P':
                    if tile.colliderect(self.rect.x + x_change, self.rect.y, self.width,
                                        self.height):
                        x_change = 0
                        hit = True

                    if tile.colliderect(self.rect.x, self.rect.y + y_change, self.width,
                                        self.height):
                        if self.velocity_y < 0:
                            self.velocity_y = 0
                            y_change = 0

                        elif self.velocity_y > 0:
                            self.velocity_y = 0
                            self.air = False
                            y_change = 0

                if block == 'L':
                    if tile.colliderect(self.rect.x, self.rect.y, self.width,
                                        self.height) and self.climbing:
                        if 240 + y * 50 + self.screen_scroll < self.rect.centerx < 240 + y * 50 + 50 + self.screen_scroll:
                            self.ladder = True
                            self.air = True
                            self.velocity_y = 0
                            y_change += -2

        if y_change > 0 and self.rect.bottom % 50 != 0:
            self.air = True

        if self.rect.left + x_change < 640 or self.rect.right + x_change > SCREEN_WIDTH - 640:
            self.screen_scroll -= x_change
            x_change = 0

        self.rect.y += y_change
        self.rect.x += x_change

        get_new_GLOBAL_X(GLOBAL_X)

        if self.cooldown > 0:
            self.cooldown -= 1

        if self.lives == 4:
            SCREEN.blit(l_4, (1435, 100))
        if self.lives == 3:
            SCREEN.blit(l_3, (1435, 100))
        if self.lives == 2:
            SCREEN.blit(l_2, (1435, 100))
        if self.lives == 1:
            SCREEN.blit(l_1, (1435, 100))

        if self.lives == 0:
            self.check_alive = False

        return [x_change, move_left, move_right, hit]

    def shoot(self):
        if self.look_direction == 1:
            return Bullet(self.rect.x + self.size[0] + self.flying_gun.get_width(),
                          self.rect.y + self.size[1] // 3 - 7,
                          5, self.look_direction, self.MAP_MATRIX, self.screen_scroll, self.actual_buff)
        return Bullet(self.rect.x - self.flying_gun.get_width(), self.rect.y + self.size[1] // 3 - 7, 5,
                      self.look_direction, self.MAP_MATRIX, self.screen_scroll, self.actual_buff)

    def get_screen_scroll(self):
        return self.screen_scroll

    def realize_buff(self, buff_type):
        self.actual_buff = buff_type
