import pygame
import os
import sys

WIDTH = 1280
HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def f_return():
    return


class Block:
    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.image = load_image(image)


class TextButton:
    def __init__(self, x, y, text, font_size, func=None, font='data/StayPixelRegular.ttf', color='black', color2='red'):
        self.font = pygame.font.Font(font, font_size)
        self.text = text
        self.color = color
        self.color_clicked = color2
        self.x = x
        self.y = y
        self.right = None
        self.bottom = None
        self.func = func

    def draw_button(self, color=None):
        if color is None:
            text_button = self.font.render(self.text, True, self.color)
        else:
            text_button = self.font.render(self.text, True, color)
        self.right = self.x + text_button.get_rect().width
        self.bottom = self.y + text_button.get_rect().height
        screen.blit(text_button, (self.x, self.y))

    def is_under(self, x, y):
        if self.x <= x <= self.right and self.y <= y <= self.bottom:
            return True
        return False

    def update(self, x, y):
        if self.is_under(x, y):
            self.draw_button(self.color_clicked)
        else:
            self.draw_button(self.color)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 70))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        # self.image = load_image('player.png')

    def jump(self):
        pass

    def is_jump(self):
        pass

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            # self.image = load_image('lplayer.png')
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
            # self.image = load_image('rplayer.png')
        if keystate[pygame.K_SPACE]:
            if not self.is_jump():
                pass
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 20))
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = 100
        self.speedx = 8
        # self.image = load_image('mouse.png')

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.speedx = -8
        if self.rect.left < 0:
            self.speedx = 8


class Dog(pygame.sprite.Sprite):
    pass
