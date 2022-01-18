import sys
import os
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


WIDTH = 1280
HEIGHT = 720
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Название")
clock = pygame.time.Clock()

click = pygame.mixer.Sound('data/click.mp3')


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Start", '',
                  "Rules",
                  "Settings"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/StayPixelRegular.ttf', 100)
    text_coord = 140
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 650
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                print(x, y, '\n')
                if 166 <= y <= 216 and 655 <= x <= 876:
                    click.play()
                    return
                if 328 <= y <= 398 and 654 <= x <= 866:
                    click.play()
                    rules_screen()
                if 419 <= y <= 486 and 654 <= x <= 990:
                    click.play()
                    settings_screen()
        pygame.display.flip()
        clock.tick(FPS)


def rules_screen():
    pass


def settings_screen():
    pass


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
            pygame.quit()
    all_sprites.update()
    screen.fill('black')
    all_sprites.draw(screen)
    pygame.display.flip()
