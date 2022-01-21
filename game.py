import pygame
import os
import sys


def load_image(name):
    fullname = os.path.join('Data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


RUN = True
WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE_WIDTH = TITLE_HEIGHT = 50

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

pygame.init()
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play()
click = pygame.mixer.Sound('data/click.mp3')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

    def jump(self):
        pass

    def is_jump(self):
        pass

    def check_col(self, col):
        if col:
            print(self.rect.right, col.rect.left)
            if col.rect.right >= self.rect.left:
                return 'col_left'
            if self.rect.right >= col.rect.left:
                return 'col_right'
            if col.rect.top <= self.rect.bottom:
                return 'col_bottom'
            if col.rect.bottom >= self.rect.top:
                return 'col_top'
        return 'OK'

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        col = pygame.sprite.spritecollideany(self, tiles_group)
        if keystate[pygame.K_LEFT] and self.check_col(col) != 'col_right':
            self.speedx = -8
            # self.image = load_image('lplayer.png')
        if keystate[pygame.K_RIGHT] and self.check_col(col) != 'col_left':
            self.speedx = 8
            # self.image = load_image('rplayer.png')
        if keystate[pygame.K_UP] and self.check_col(col) != 'col_bottom':
            self.speedy = -8
        if keystate[pygame.K_DOWN] and self.check_col(col) != 'col_top':
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        # self.image = tile_images[tile_type]
        self.image = pygame.Surface((TITLE_HEIGHT, TITLE_WIDTH))
        self.image.fill('green')
        self.rect = self.image.get_rect().move(
            TITLE_WIDTH * pos_x, TITLE_HEIGHT * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def start_screen():
    global PAUSED, RUN
    PAUSED = False
    RUN = False
    all_sprites.empty()
    buttons = [TextButton(655, 166, 'Start', 100, game), TextButton(655, 328, 'Rules', 100, rules_screen),
               TextButton(655, 419, 'Settings', 100, settings_screen)]
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

    button = TextButton(0, 0, 'Back', 100, start_screen)
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
