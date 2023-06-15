import pygame

clock = pygame.time.Clock()
FPS = 60
G = 0.5

CHARACTER_SPEED = 5


class DropCrate(pygame.sprite.Sprite):
    def __init__(self, x, y, drop_type, screen_scroll, direction, MAP_MATRIX):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../Textures/drop_crate_empty.png')
        if drop_type == 1:
            self.image = pygame.image.load('../Textures/drop_crate_acceleration.png')
        elif drop_type == 2:
            self.image = pygame.image.load('../Textures/drop_crate_damage.png')
        else:
            self.image = pygame.image.load('../Textures/drop_crate_size.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.drop_type = drop_type
        self.velocity_x = 10
        self.velocity_y = -10
        self.screen_scroll = screen_scroll
        self.MAP_MATRIX = MAP_MATRIX

        self.size = self.image.get_size()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.direction = 0
        if direction == 1:
            self.direction = -1
        else:
            self.direction = 1

        self.velocity_x *= self.direction
        self.condition = 'not static'

    def update(self, change, char, screen_scroll):
        self.screen_scroll = screen_scroll
        global CHARACTER_SPEED
        if change[0] == 0 and change[1] and not change[3]:
            self.rect.x += CHARACTER_SPEED
        if change[0] == 0 and change[2] and not change[3]:
            self.rect.x -= CHARACTER_SPEED
        if self.condition != 'static':
            if self.velocity_y > 12:
                self.velocity_y = 12

            self.velocity_y += G
            if self.velocity_x:
                self.velocity_x -= 0.5 * G * self.direction

            if abs(self.velocity_x) <= 1 and self.velocity_x and self.velocity_y:
                self.velocity_x = self.direction

            x_change = 0
            if self.velocity_x:
                x_change = self.direction * self.velocity_x
            y_change = self.velocity_y

            for x in range(len(self.MAP_MATRIX)):
                for y in range(len(self.MAP_MATRIX[x])):
                    block = self.MAP_MATRIX[x][y]
                    tile = pygame.Rect((240 + y * 50 + self.screen_scroll, x * 50), (50, 50))

                    if block == 'P':
                        if tile.colliderect(self.rect.x + x_change, self.rect.y, self.width,
                                            self.height):
                            x_change = 0
                            self.velocity_x = 0

                        if tile.colliderect(self.rect.x, self.rect.y + y_change, self.width,
                                            self.height):
                            if self.velocity_y < 0:
                                self.velocity_y = abs(self.velocity_y)
                                y_change = 0

                            elif self.velocity_y > 0:
                                self.velocity_y = 0
                                self.velocity_x = 0
                                y_change = 0
                                x_change = 0
                                self.condition = 'static'

            self.rect.x += x_change
            self.rect.y += y_change

        if self.rect.colliderect(char.rect):
            self.kill()
            requests3_copy = open('../Other/info-flows/flow_03.txt', 'w')
            requests3_copy.write(str(self.drop_type) + '\n')
            requests3_copy.close()
