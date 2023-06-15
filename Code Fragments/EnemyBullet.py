import pygame

CHARACTER_SPEED = 5


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, direction, MAP_MATRIX, screen_scroll):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../Textures/enemy_bullet.png")
        self.speed = speed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.direction = direction
        self.MAP_MATRIX = MAP_MATRIX
        self.screen_scroll = screen_scroll

    def update(self, change, char, screen_scroll):
        self.screen_scroll = screen_scroll
        if change[0] == 0 and change[1] and not change[3]:
            if self.direction == 1:
                self.rect.x += self.speed + CHARACTER_SPEED
            else:
                self.rect.x -= self.speed - CHARACTER_SPEED
        else:
            if self.direction == 1:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
        if change[0] == 0 and change[2] and not change[3]:
            if self.direction == 1:
                self.rect.x += self.speed - CHARACTER_SPEED
            else:
                self.rect.x -= self.speed + CHARACTER_SPEED
        else:
            if self.direction == 1:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        for x in range(len(self.MAP_MATRIX)):
            for y in range(len(self.MAP_MATRIX[x])):
                block = self.MAP_MATRIX[x][y]
                tile = pygame.Rect((240 + y * 50 + self.screen_scroll, x * 50), (50, 50))

                if block == 'P':
                    if tile.colliderect(self.rect.x + self.speed, self.rect.y, self.rect.width,
                                        self.rect.height):
                        self.kill()

        if abs(char.rect.x - self.rect.x) > 1600:
            self.kill()

        if self.rect.colliderect(char.rect):
            char.lives -= 1
            self.kill()
