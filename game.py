from GameSprites import *

PAUSED = False

pygame.display.set_caption("Cats")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play()
click = pygame.mixer.Sound('data/click.mp3')


def start_screen():
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


def levels():
    pass


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


def pause_menu():
    fon = pygame.transform.scale(load_image('menu.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (WIDTH // 2, HEIGHT // 2))

    button = TextButton(0, 0, 'Back', 100, start_screen())
    button.draw_button()
    while True:
        global PAUSED
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
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_ESCAPE]:
                PAUSED = not PAUSED
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
player = Player()
mouse = Mouse()
all_sprites.add(mouse)
all_sprites.add(player)
start_screen()


def game():
    global PAUSED
    fon = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_ESCAPE]:
                pause_menu()
                PAUSED = not PAUSED
        if not PAUSED:
            all_sprites.update()
            screen.blit(fon, (0, 0))
            all_sprites.draw(screen)
            pygame.display.flip()

game()
