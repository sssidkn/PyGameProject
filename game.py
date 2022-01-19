import sys
import os
import pygame

WIDTH = 1280
HEIGHT = 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Cats")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play(loops=-1)
click = pygame.mixer.Sound('data/click.mp3')


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

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            # self.image = load_image('lplayer.png')
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
            # self.image = load_image('rplayer.png')
        # if keystate[pygame.K_SPACE]:
        # TODO: JUMP
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


def start_screen():
    pygame.init()
    buttons = [TextButton(655, 166, 'Start', 100, f_return), TextButton(655, 328, 'Rules', 100, rules_screen),
               TextButton(655, 419, 'Settings', 100, settings_screen)]
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/StayPixelRegular.ttf', 100)
    for button in buttons:
        button.draw_button()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                for button in buttons:
                    if button.is_under(x, y):
                        click.play()
                        button.func()
                        return
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                for button in buttons:
                    button.update(x, y)
        pygame.display.flip()
        clock.tick(FPS)


def rules_screen():
    text = ['', 'Catch mice', 'Collect fish', 'Avoid dogs']

    fon = pygame.transform.scale(load_image('rules.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font('data/StayPixelRegular.ttf', 100)

    button = TextButton(0, 0, 'Back', 100, start_screen)

    font = pygame.font.Font('data/StayPixelRegular.ttf', 70)
    string_rendered = font.render('Rules', 1, pygame.Color('black'))
    screen.blit(string_rendered, (WIDTH // 2 - 100, 80))

    font = pygame.font.Font('data/StayPixelRegular.ttf', 50)
    text_coord = 140
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    button.draw_button()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if button.is_under(x, y):
                    click.play()
                    button.func()
                    return
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                button.update(x, y)
        pygame.display.flip()
        clock.tick(FPS)


def settings_screen():
    fon = pygame.transform.scale(load_image('settings.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    button = TextButton(0, 0, 'Back', 100, start_screen)
    button.draw_button()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if button.is_under(x, y):
                    button.func()
                    return
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                button.update(x, y)
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
player = Player()
mouse = Mouse()
all_sprites.add(mouse)
all_sprites.add(player)

start_screen()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    all_sprites.update()
    screen.fill('black')
    all_sprites.draw(screen)
    pygame.display.flip()
