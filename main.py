import pygame as pg
import random

pg.init()

screen_width, screen_height = 800, 600

FPS = 24    # frame per second
clock = pg.time.Clock()

# изображения
bg_img = pg.image.load('background.png')
icon_img = pg.image.load('ufo.png')

display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Космическое вторжение')

# display.fill('blue', (0, 0, screen_width, screen_height))
display.blit(bg_img, (0, 0))        # image.tr

# text_img = sys_font.render('Score 123', True, 'white')
# display.blit(text_img, (100, 50))

def enemy_create():
    """ Создаем противника в случайном месте вверху окна."""
    global enemy_y, enemy_x
    enemy_x = random.randint(0, screen_width - enemy_width - 10)   # screen_width / 2 - enemy_width / 2
    enemy_y = 0
    print(f'CREATE: {enemy_x=}')

def model_update():
    palayer_model_x()
    palayer_model_y()
    bullet_model()
    enemy_model()

def palayer_model_x():
    global player_x
    player_x += player_dx
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_width:
        player_x = screen_width - player_width

def palayer_model_y():
    global player_y
    player_y += player_dy
    if player_y < 0:
        player_y = 0
    elif player_y > screen_height - player_height:
        player_y = screen_height - player_height

def bullet_model():
    """ Изменяется положение пули. """
    global bullet_y, bullet_alive
    bullet_y += bullet_dy
    # пуля улетела за верх экрана
    if bullet_y < 0:
        bullet_alive = False

def bullet_create():
    global bullet_y, bullet_x, bullet_alive
    bullet_alive = True
    bullet_x = player_x + bullet_width/2 # микро дз - пускать из середины
    bullet_y = player_y - bullet_height

def enemy_model():
    """ Изменение положения противника, рассчет поражений."""
    global enemy_y, enemy_x, bullet_alive, enemy_dy, life, life_text, enemy_dx
    enemy_x += enemy_dx*4
    enemy_y += enemy_dy
    if enemy_y > screen_height:
        enemy_create()
        life -= 1
        life_text = life_font.render(f'Жизни: {str(life)}', True, 'White')
    if enemy_x >= screen_width-enemy_width or enemy_x <= 0:
        enemy_dx *= -1

    # пересечение с пулей
    if bullet_alive:
        re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rb = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
        is_crossed = re.colliderect(rb)
        # попал!
        if is_crossed:
            # изменение направления движения и скорости врага
            enemy_dx = random.randint(-1,1)
            enemy_create()
            bullet_alive = False
            score_up()
            if enemy_dy < 6:
                enemy_dy += 0.6

def score_up():
    global score,score_text
    score += 10
    score_text = score_font.render(f'Очки: {str(score)}', True, 'White')

def ending():
    re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    rb = pg.Rect(player_x, player_y, player_width, player_height)
    is_crossed = re.colliderect(rb)
    if is_crossed:
        return False
    if life == 0:
        return False
    else:
        return True


def display_redraw():
    display.blit(bg_img, (0, 0))
    display.blit(player_img, (player_x, player_y))
    display.blit(enemy_img, (enemy_x, enemy_y))
    display.blit(score_text, (10, 10))
    display.blit(life_text, (screen_width-100,10))
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))
    pg.display.update()

def event_processing():
    global player_dx,player_dy, restart
    running = True
    for event in pg.event.get():
        # нажали крестик на окне
        if event.type == pg.QUIT:
            running = False
            restart = False
        # тут нажимаем на клавиши
        if event.type == pg.KEYDOWN:
            # нажали на q - quit
            if event.key == pg.K_q:
                running = False
        # движение игрока
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                player_dx = -player_velocity
            elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                player_dx = player_velocity
            elif event.key == pg.K_w:
                player_dy = -player_velocity
            elif event.key == pg.K_s:
                player_dy = player_velocity
        if event.type == pg.KEYUP:
            player_dx = 0
            player_dy = 0

        # по левому клику мыши стреляем
        if event.type == pg.MOUSEBUTTONDOWN:
            key = pg.mouse.get_pressed()    # key[0] - left, key[2] - right
            print(f'{key[0]=} {bullet_alive=}')
            if not bullet_alive:
                bullet_create()

    clock.tick(FPS)
    return running

# random.seed(77)

restart = True
while restart:
    running = True
    # игрок
    player_img = pg.image.load('player.png')
    player_width, player_height = player_img.get_size()
    player_gap = 10
    player_velocity = 10
    player_dx = 0
    player_dy = 0
    player_x = screen_width / 2 - player_width / 2
    player_y = screen_height - player_height - player_gap

    # пуля
    bullet_img = pg.image.load('bullet.png')
    bullet_width, bullet_height = bullet_img.get_size()
    bullet_dy = -20
    bullet_x = 0  # микро дз - пускать из середины
    bullet_y = 0
    bullet_alive = False  # есть пуля?

    # противник
    enemy_img = pg.image.load('enemy.png')
    enemy_width, enemy_height = enemy_img.get_size()
    enemy_dx = 0
    enemy_dy = 2
    enemy_x = 0
    enemy_y = 0

    # Жизни
    life = 3
    life_font = pg.font.SysFont('Times New Roman', 24)
    life_text = life_font.render(f'Жизни: {str(life)}', True, 'White')

    # Очки
    score = 0
    score_font = pg.font.SysFont('Times New Roman', 24)
    score_text = score_font.render(f'Очки: {str(score)}', True, 'White')

    enemy_create()
    while running:
        model_update()
        display_redraw()
        running = min(event_processing(),ending())

    display.blit(bg_img, (0,0))
    #текст при поражении
    ## R
    restart_text = (pg.font.SysFont('04B_19.TTF',32))
    restart_text_display = restart_text.render('Нажмите "R", чтобы продолжить',True, 'White')
    w_restart_text, h_restart_text = restart_text_display.get_size()
    display.blit(restart_text_display, (screen_width/2-w_restart_text/2,screen_height/2-h_restart_text/2))
    ## Q
    restart_text_display = restart_text.render('Нажмите "Q", чтобы выйти ',True, 'White')
    w_restart_text, h_restart_text = restart_text_display.get_size()
    display.blit(restart_text_display, (screen_width/2-w_restart_text/2,screen_height/2-h_restart_text/2+h_restart_text))
    ## Game Over
    font = pg.font.Font('04B_19.TTF', 48)
    game_over_text = font.render('Game Over', True, 'red')
    w, h = game_over_text.get_size()
    display.blit(game_over_text, (screen_width/2 - w/2, screen_height / 2 - h/2 - h_restart_text*2))
    pg.display.update()
    flag = True

    # Обработка нажатия клавиш для выхода
    while flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag = False
                restart = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    restart = True
                    flag = False
                elif event.key == pg.K_q:
                    restart = False
                    flag = False
pg.quit()
