import pygame
import os
import sys

RUN = True
FPS = 60
K_VOLUME = 0.5
TITLE_WIDTH = TITLE_HEIGHT = 50
GRAVITI = 0.5


def load_image(name):
    fullname = os.path.join('Data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


player = None
all_sprites = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

pygame.init()
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play()
click = pygame.mixer.Sound('data/click.mp3')

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()

tile_images = {
    'wall': load_image('snow.png')
}


# player_image = load_image('player.png')


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "Data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def f_continue():
    global PAUSED
    PAUSED = not PAUSED
    return


def f_return():
    return


def f_exit():
    global RUN
    RUN = False
    return


def plus_volume():
    global K_VOLUME
    K_VOLUME = min(1, K_VOLUME + 0.1)
    pygame.mixer.music.set_volume(K_VOLUME)


def minus_volume():
    global K_VOLUME
    K_VOLUME = max(0, K_VOLUME + 0.1)
    pygame.mixer.music.set_volume(K_VOLUME)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


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
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.Surface((50, 100))
        self.image.fill('red')
        # self.image = player_image
        self.rect = self.image.get_rect().move(
            TITLE_WIDTH * pos_x + 15, TITLE_HEIGHT * pos_y - TITLE_HEIGHT)
        self.onGround = False

    def collide(self):
        global platforms_group
        for platform in platforms_group:
            if pygame.sprite.collide_rect(self, platform):
                if self.speedx > 0:
                    self.rect.right = platform.rect.left
                if self.speedx < 0:
                    self.rect.left = platform.rect.right
                if self.speedy > 0:
                    self.rect.bottom = platform.rect.top
                    self.onGround = True
                    self.speedy = 0
                if self.speedy < 0:
                    self.rect.top = platform.rect.bottom
                    self.speedy = 0

    def jump(self):
        if self.onGround:
            self.onGround = False

    def update(self):
        global platforms_group
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
            # self.image = load_image('lplayer.png')
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
            # self.image = load_image('rplayer.png')
        elif keystate[pygame.K_SPACE]:
            self.jump()

        self.rect.x += self.speedx
        self.collide()
        self.rect.y += self.speedy
        self.collide()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(platforms_group, all_sprites)
        # self.image = tile_images[tile_type]
        self.image = pygame.Surface((TITLE_HEIGHT, TITLE_WIDTH))
        self.image.fill('green')
        self.rect = self.image.get_rect().move(
            TITLE_WIDTH * pos_x, TITLE_HEIGHT * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def start_screen():
    global PAUSED, RUN
    PAUSED = False
    RUN = False
    all_sprites.empty()
    buttons = [TextButton(WIDTH / 2.15, HEIGHT / 5.2, 'Start', 120, game),
               TextButton(WIDTH / 2.15, HEIGHT / 3.2, 'Rules', 120, rules_screen),
               TextButton(WIDTH / 2.15, HEIGHT / 2.3, 'Settings', 120, settings_screen),
               TextButton(WIDTH / 2.15, HEIGHT / 1.8, 'Exit', 130, terminate)]
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
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

    button = TextButton(0, 0, 'Back', 100, start_screen)

    font = pygame.font.Font('data/StayPixelRegular.ttf', 70)
    string_rendered = font.render('Rules', True, pygame.Color('black'))
    screen.blit(string_rendered, (WIDTH // 2 - 100, 80))

    font = pygame.font.Font('data/StayPixelRegular.ttf', 50)
    text_coord = 140
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('black'))
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
    buttons = [TextButton(0, 0, 'Back', 120, start_screen),
               TextButton(WIDTH // 2, HEIGHT // 2, '<-', 100, plus_volume),
               TextButton(WIDTH // 2 + 100, HEIGHT // 2, '<-', 100, minus_volume)]
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


def pause_menu():
    global PAUSED
    fon = pygame.transform.scale(load_image('menu.png'), (500, 500))
    screen.blit(fon, (WIDTH // 2 - 250, HEIGHT // 2 - 250))

    continue_btn = TextButton(WIDTH // 2 - 170, HEIGHT // 2, 'Continue', 100, f_continue)
    continue_btn.draw_button()
    settings_btn = TextButton(WIDTH // 2 - 170, HEIGHT // 2 - 100, 'Menu', 100, start_screen)
    settings_btn.draw_button()
    buttons = [continue_btn, settings_btn]
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
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_ESCAPE]:
                PAUSED = not PAUSED
                return
        pygame.display.flip()
        clock.tick(FPS)


def game():
    global PAUSED, RUN
    fon = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    player, level_x, level_y = generate_level(load_level('map.txt'))
    camera = Camera()
    RUN = True
    while RUN:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                terminate()
            if keystate[pygame.K_ESCAPE]:
                pause_menu()
                PAUSED = not PAUSED
        if not PAUSED:
            all_sprites.update()
            screen.blit(fon, (0, 0))
            all_sprites.draw(screen)
            pygame.display.flip()
            camera.update(player)
            for s in all_sprites:
                camera.apply(s)
    return


start_screen()
