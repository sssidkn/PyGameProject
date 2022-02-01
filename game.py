import pygame
import os
import sys

RUN = True
FPS = 60
K_VOLUME = 0.5
TILES_WIDTH = 50
TILES_HEIGHT = 50
GRAVITY = 0.95
PLAYER_SPEED = 8
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 80
ANIM_COUNT = 0
N_LEVELS = 2
JUMP_POWER = 13
CURR_LEVEL = 1
WIN_LEVELS = []
with open('Data/win_levels', 'r', encoding='utf-8') as win:
    for level in win.readlines():
        WIN_LEVELS.append(level.strip())


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
items_group = pygame.sprite.Group()

pygame.init()
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('data/music/music.mp3')
pygame.mixer.music.play(loops=-1)
click = pygame.mixer.Sound('data/music/click.mp3')

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()

images = {
    'platform': pygame.transform.scale(load_image('pic/grassHalfMid.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'ground': pygame.transform.scale(load_image('pic/ground.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'stone': pygame.transform.scale(load_image('pic/dirtCenter.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'grass': pygame.transform.scale(load_image('pic/Grass.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'close_door': pygame.transform.scale(load_image('pic/door_closedMid.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'close_door_top': pygame.transform.scale(load_image('pic/door_closedTop.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'open_door': pygame.transform.scale(load_image('pic/door_openMid.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'open_door_top': pygame.transform.scale(load_image('pic/door_openTop.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'coin': pygame.transform.scale(load_image('pic/CoinGold.png'), (TILES_WIDTH, TILES_HEIGHT)),
    'key': pygame.transform.scale(load_image('pic/KeyRed.png'), (TILES_WIDTH, TILES_HEIGHT))
}

player_go_right = []
player_go_left = []
for i in range(1, 11):
    image = load_image(f'player_go/Walk ({i}).png')
    image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
    player_go_right.append(image)
    player_go_left.append(pygame.transform.flip(image, True, False))
player_stay_right = pygame.transform.scale(load_image('pic/Stay.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
player_stay_left = pygame.transform.flip(player_stay_right, True, False)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "Data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def f_continue():
    global PAUSED
    PAUSED = not PAUSED
    return


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '_':
                Tile('platform', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '/':
                Tile('stone', x, y)
            elif level[y][x] == '#':
                Tile('grass', x, y)
            elif level[y][x] == '|':
                Tile('ground', x, y)
            elif level[y][x] == '?':
                Tile('coin', x, y)
            elif level[y][x] == 'k':
                Tile('key', x, y)
            elif level[y][x] == '}':
                Tile('close_door', x, y)
            elif level[y][x] == ']':
                Tile('close_door_top', x, y)
            elif level[y][x] == '{':
                Tile('open_door', x, y)
            elif level[y][x] == '[':
                Tile('open_door_top', x, y)
    return new_player, x, y


class TextButton:
    def __init__(self, x, y, text, font_size, func=None, font='data/fonts/StayPixelRegular.ttf', color=(0, 0, 0),
                 color2=(255, 0, 0)):
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


class Button(TextButton):
    def draw_button(self, color=None):
        if self.text in WIN_LEVELS:
            text_button = self.font.render(self.text, True, 'green')
        elif color is None:
            text_button = self.font.render(self.text, True, self.color)
        else:
            text_button = self.font.render(self.text, True, color)
        self.right = self.x + text_button.get_rect().width
        self.bottom = self.y + text_button.get_rect().height
        pygame.draw.circle(screen, 'blue', (self.x + text_button.get_rect().width // 2, self.y // 2 + self.bottom // 2),
                           50, 5)
        screen.blit(text_button, (self.x, self.y))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_stay_right, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect().move(
            TILES_WIDTH * pos_x, pos_y * TILES_HEIGHT)
        self.right = True
        self.left = False
        self.keys = 0
        self.coins = 0
        self.speedy = 0
        self.speedx = 0

    def calc_gravity(self):
        if not self.speedy:
            self.speedy = 1
        else:
            self.speedy += GRAVITY
        if self.rect.y >= HEIGHT - self.rect.height and self.speedy >= 0:
            self.speedy = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += JUMP_POWER
        platform_hit_list = pygame.sprite.spritecollide(self, platforms_group, False)
        self.rect.y -= JUMP_POWER
        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.speedy = -JUMP_POWER - 5

    def go_right(self):
        self.speedx = PLAYER_SPEED
        if not self.right:
            self.image = pygame.transform.flip(self.image, True, False)
            self.right = True
            self.left = False

    def go_left(self):
        self.speedx = -PLAYER_SPEED
        if self.right:
            self.image = player_go_left[ANIM_COUNT // 6]
            self.right = False
            self.left = True

    def stay(self):
        self.speedx = 0
        if self.right:
            self.image = player_stay_right
        else:
            self.image = player_stay_left

    def update(self):
        global platforms_group, GRAVITY, ANIM_COUNT
        ANIM_COUNT += 1
        if ANIM_COUNT >= 60:
            ANIM_COUNT = 0
        if self.right and self.speedx != 0:
            self.image = player_go_right[ANIM_COUNT // 6]
        elif self.left and self.speedx != 0:
            self.image = player_go_left[ANIM_COUNT // 6]
        self.calc_gravity()
        self.rect.x += self.speedx
        hit_list = pygame.sprite.spritecollide(self, platforms_group, False)
        for block in hit_list:
            if ((block.type == 'close_door' or block.type == 'close_door_top') and self.keys == 3) or (
                    block.type == 'open_door' or block.type == 'open_door_top'):
                game_over()
            else:
                if self.speedx > 0:
                    self.rect.right = block.rect.left
                elif self.speedx < 0:
                    self.rect.left = block.rect.right
        self.rect.y += self.speedy
        hit_list = pygame.sprite.spritecollide(self, platforms_group, False)
        for block in hit_list:
            if ((block.type == 'close_door' or block.type == 'close_door_top') and self.keys == 3) or (
                    block.type == 'open_door' or block.type == 'open_door_top'):
                game_over()
            else:
                if self.speedy > 0:
                    self.rect.bottom = block.rect.top
                elif self.speedy < 0:
                    self.rect.top = block.rect.bottom
                self.speedy = 0
        item = pygame.sprite.spritecollide(self, items_group, True)
        if item is not None:
            for i in item:
                if i.type == 'coin':
                    self.coins += 1
                elif i.type == 'key':
                    self.keys += 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.type = tile_type
        self.image = pygame.Surface((TILES_HEIGHT, TILES_WIDTH))
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(
            TILES_WIDTH * pos_x, TILES_HEIGHT * pos_y)
        if tile_type == 'coin' or tile_type == 'key':
            items_group.add(self)
        else:
            all_sprites.add(self)
            platforms_group.add(self)


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
    items_group.empty()
    platforms_group.empty()
    player_group.empty()
    buttons = [TextButton(WIDTH / 2.15, HEIGHT / 5.2, 'Start', 120, levels),
               TextButton(WIDTH / 2.15, HEIGHT / 3.2, 'Rules', 120, rules_screen),
               TextButton(WIDTH / 2.15, HEIGHT / 1.8, 'Exit', 130, terminate)]
    fon = pygame.transform.scale(load_image('pic/fon.png'), (WIDTH, HEIGHT))
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


def levels():
    global CURR_LEVEL
    all_sprites.empty()
    items_group.empty()
    platforms_group.empty()
    player_group.empty()
    buttons = []
    fon = pygame.transform.scale(load_image('pic/levels.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_back = TextButton(0, 0, 'Back', 100, start_screen)
    button_back.draw_button()
    x = 70
    y = 100
    for i in range(1, N_LEVELS + 1):
        buttons.append(Button(x, y, str(i), 60, game, font='data/fonts/IBMPlexSansThaiLooped-SemiBold.ttf'))
        buttons[i - 1].draw_button()
        x = buttons[i - 1].right + 100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                for button in buttons:
                    if button.is_under(x, y):
                        click.play()
                        CURR_LEVEL = int(button.text)
                        button.func()
                        return
                if button_back.is_under(x, y):
                    button_back.func()
                    return
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                for button in buttons:
                    button.update(x, y)
                button_back.update(x, y)
        pygame.display.flip()
        clock.tick(FPS)


def next_level():
    global CURR_LEVEL, N_LEVELS
    if CURR_LEVEL + 1 <= N_LEVELS:
        CURR_LEVEL += 1
        all_sprites.empty()
        items_group.empty()
        platforms_group.empty()
        player_group.empty()
        game()


def restart():
    global PAUSED, RUN
    RUN = False
    PAUSED = False
    all_sprites.empty()
    items_group.empty()
    platforms_group.empty()
    player_group.empty()
    game()


def game_over():
    global player, CURR_LEVEL
    if CURR_LEVEL not in WIN_LEVELS:
        WIN_LEVELS.append(str(CURR_LEVEL))
        with open('Data/win_levels', 'w', encoding='utf-8') as win:
            win.writelines(line + '\n' for line in WIN_LEVELS)
    fon = pygame.transform.scale(load_image('pic/gameover.png'), (575, 557))
    screen.blit(fon, (WIDTH // 2 - 300, HEIGHT // 2 - 300))
    font = pygame.font.Font('data/fonts/IBMPlexSansThaiLooped-SemiBold.ttf', 90)
    text = font.render(f'Score: {player.coins}', True, 'black')
    screen.blit(text, (WIDTH // 2 - 250, HEIGHT // 2 - 250))
    restart_btn = TextButton(WIDTH // 2 - 250, HEIGHT // 2 - 100, 'Restart', 120, restart)
    restart_btn.draw_button()
    exit_btn = TextButton(WIDTH // 2 - 250, HEIGHT // 2 + 100, 'Menu', 120, start_screen)
    exit_btn.draw_button()
    next_btn = TextButton(WIDTH // 2 - 250, HEIGHT // 2, 'Next level', 120, next_level)
    next_btn.draw_button()
    buttons = [restart_btn, next_btn, exit_btn]
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
    text = ['', 'Collect coins', 'Collect keys']

    fon = pygame.transform.scale(load_image('pic/rules.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    button = TextButton(0, 0, 'Back', 100, start_screen)

    font = pygame.font.Font('data/fonts/StayPixelRegular.ttf', 70)
    string_rendered = font.render('Rules', True, pygame.Color('black'))
    screen.blit(string_rendered, (WIDTH // 2 - 100, 80))

    font = pygame.font.Font('data/fonts/StayPixelRegular.ttf', 50)
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


def pause_menu():
    global PAUSED
    fon = pygame.transform.scale(load_image('pic/menu.png'), (500, 500))
    screen.blit(fon, (WIDTH // 2 - 250, HEIGHT // 2 - 250))
    continue_btn = TextButton(WIDTH // 2 - 170, HEIGHT // 2 - 25, 'Continue', 100, f_continue)
    continue_btn.draw_button()
    menu_btn = TextButton(WIDTH // 2 - 170, HEIGHT // 2 - 125, 'Menu', 100, start_screen)
    menu_btn.draw_button()
    back_btn = TextButton(WIDTH // 2 - 170, HEIGHT // 2 + 75, 'Back', 100, levels)
    back_btn.draw_button()
    restart_btn = TextButton(WIDTH // 2 - 170, HEIGHT // 2 + 175, 'Restart', 100, restart)
    restart_btn.draw_button()
    buttons = [continue_btn, menu_btn, back_btn, restart_btn]
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
    global PAUSED, RUN, CURR_LEVEL, player
    fon = pygame.transform.scale(load_image('pic/background.png').convert(), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    player, level_x, level_y = generate_level(load_level(f'level_{CURR_LEVEL}'))
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
            if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
                player.go_left()
            if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
                player.go_right()
            if keystate[pygame.K_UP] or keystate[pygame.K_SPACE]:
                player.jump()
            if not (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and not (
                    keystate[pygame.K_LEFT] or keystate[pygame.K_a]):
                player.stay()
        if not PAUSED:
            all_sprites.update()
            screen.blit(fon, (0, 0))
            all_sprites.draw(screen)
            items_group.draw(screen)
            pygame.display.flip()
            camera.update(player)
            for s in all_sprites:
                camera.apply(s)
            for item in items_group:
                camera.apply(item)


if __name__ == '__main__':
    start_screen()
