import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CHARACTER_SPEED = 5


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, difficulty):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.difficulty = difficulty
        self.image = pygame.image.load(f'../Textures/portal_{difficulty}.png')
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

    def check_completion(self, character):
        if self.rect.colliderect(character.rect.x - character.width // 2, character.rect.y, character.width,
                                 character.height):
            return True

    def draw(self):
        SCREEN.blit(self.image, self.rect)

    def update(self, change):
        if change[0] == 0 and change[1] and not change[3]:
            self.rect.x += CHARACTER_SPEED
        if change[0] == 0 and change[2] and not change[3]:
            self.rect.x -= CHARACTER_SPEED
