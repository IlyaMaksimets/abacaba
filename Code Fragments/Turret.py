import pygame
import mysql.connector

from EnemyBullet import EnemyBullet

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CHARACTER_SPEED = 5

TURRETS_DESTROYED = 0

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


class Turret(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, health, bullet_speed, MAP_MATRIX, CHOSEN_DIFFICULTY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../Textures/turret.png')
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.x = pos_x
        self.y = pos_y
        self.size = self.image.get_size()
        self.health = health
        self.look_direction = -1
        self.change_direction = False
        self.cooldown = 60 - CHOSEN_DIFFICULTY * 5
        self.chosen_difficulty = CHOSEN_DIFFICULTY
        self.bullet_speed = bullet_speed
        self.MAP_MATRIX = MAP_MATRIX

    def shoot(self):
        if self.look_direction == 1:
            return EnemyBullet(self.rect.x + self.size[0], self.rect.y + self.size[1] // 3 + 9,
                               self.bullet_speed, self.look_direction, self.MAP_MATRIX)
        return EnemyBullet(self.rect.x, self.rect.y + self.size[1] // 3 + 9, self.bullet_speed,
                           self.look_direction, self.MAP_MATRIX)

    def update(self, change, char):
        if change[0] == 0 and change[1] and not change[3]:
            self.rect.x += CHARACTER_SPEED
        if change[0] == 0 and change[2] and not change[3]:
            self.rect.x -= CHARACTER_SPEED

        if (char.rect.right + 20 < self.rect.left) and abs(self.rect.bottom - char.rect.bottom) < 50:
            self.look_direction = -1
            self.change_direction = False
        if (char.rect.left - 20 > self.rect.right) and abs(self.rect.bottom - char.rect.bottom) < 50:
            self.look_direction = 1
            self.change_direction = True

        SCREEN.blit(pygame.transform.flip(self.image, self.change_direction, False), self.rect)

        if self.health < 1:
            destruction_sound = pygame.mixer.Sound("../Sounds/destruction_sound.mp3")
            destruction_sound.play()
            destruction_sound.set_volume(SOUNDS_VOLUME / 100)
            global TURRETS_DESTROYED
            TURRETS_DESTROYED += 1
            requests_copy = open('../Other/info-flows/flow_02.txt', 'w')
            requests_copy.write(str(self.rect.x) + '\n')
            requests_copy.write(str(self.rect.y) + '\n')
            requests_copy.close()
            self.kill()

        if 0 < self.rect.left - char.rect.right < 700 and abs(self.rect.bottom - char.rect.bottom) < 50:
            if self.cooldown > 0:
                self.cooldown -= 1
            if self.cooldown == 0:
                self.cooldown = 60 - self.chosen_difficulty * 5
                if self.look_direction == 1:
                    requests_copy = open('../Other/info-flows/flow_01.txt', 'w')
                    requests_copy.write(str(self.rect.x + self.size[0]) + '\n')
                    requests_copy.write(str(self.rect.y + self.size[1] // 3 + 9) + '\n')
                    requests_copy.write(str(self.bullet_speed) + '\n')
                    requests_copy.write(str(self.look_direction) + '\n')
                    requests_copy.close()
                else:
                    requests_copy = open('../Other/info-flows/flow_01.txt', 'w')
                    requests_copy.write(str(self.rect.x) + '\n')
                    requests_copy.write(str(self.rect.y + self.size[1] // 3 + 9) + '\n')
                    requests_copy.write(str(self.bullet_speed) + '\n')
                    requests_copy.write(str(self.look_direction) + '\n')
                    requests_copy.close()

        if 0 < char.rect.left - self.rect.right < 700 and abs(self.rect.bottom - char.rect.bottom) < 50:
            if self.cooldown > 0:
                self.cooldown -= 1
            if self.cooldown == 0:
                self.cooldown = 60 - self.chosen_difficulty * 5
                if self.look_direction == 1:
                    requests_copy = open('../Other/info-flows/flow_01.txt', 'w')
                    requests_copy.write(str(self.rect.x + self.size[0]) + '\n')
                    requests_copy.write(str(self.rect.y + self.size[1] // 3 + 9) + '\n')
                    requests_copy.write(str(self.bullet_speed) + '\n')
                    requests_copy.write(str(self.look_direction) + '\n')
                    requests_copy.close()
                else:
                    requests_copy = open('../Other/info-flows/flow_01.txt', 'w')
                    requests_copy.write(str(self.rect.x) + '\n')
                    requests_copy.write(str(self.rect.y + self.size[1] // 3 + 9) + '\n')
                    requests_copy.write(str(self.bullet_speed) + '\n')
                    requests_copy.write(str(self.look_direction) + '\n')
                    requests_copy.close()
