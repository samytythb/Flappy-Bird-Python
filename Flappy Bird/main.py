import pygame
import sys
import random
pygame.init()


def draw_floor():
    screen.blit(floor2x, (floor_x_pos, 650))
    screen.blit(floor2x, (floor_x_pos+432, 650))


def create_pipe():
    random_pos = random.choice(pipe_height)
    bot_pipe = pipe2x.get_rect(midtop=(500, random_pos))
    top_pipe = pipe2x.get_rect(midtop=(500, random_pos-700))
    return bot_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 500:
            screen.blit(pipe2x, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe2x, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird2x_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird2x_rect.top <= -75 or bird2x_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird2x):
    new_bird = pygame.transform.rotozoom(bird2x, -bird_movement*3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird2x_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(
            str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.display.set_caption("Flappy Bird")
# xet dai rong cho man hinh hien thi
screen = pygame.display.set_mode((432, 768))
# xet do nhanh cham khi bird di chuyen
clock = pygame.time.Clock()
gravity = 0.2
bird_movement = 0
game_active = True
game_font = pygame.font.Font('Projects/Flappy Bird/04B_19.TTF', 35)
score = 0
high_score = 0
background = pygame.image.load(
    "Projects/Flappy Bird/assets/background-night.png").convert()
background2x = pygame.transform.scale2x(background)
floor = pygame.image.load(
    "Projects/Flappy Bird/assets/floor.png").convert()
floor2x = pygame.transform.scale2x(floor)
floor_x_pos = 0
bird_down = pygame.transform.scale2x(pygame.image.load(
    'Projects/Flappy Bird/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load(
    'Projects/Flappy Bird/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load(
    'Projects/Flappy Bird/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]  # 0 1 2
# bird = pygame.image.load(
#     "Projects/Flappy Bird/assets/yellowbird-midflap.png").convert_alpha()
# bird2x = pygame.transform.scale2x(bird)
bird_index = 0
bird2x = bird_list[bird_index]
bird2x_rect = bird2x.get_rect(center=(100, 384))
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
pipe = pygame.image.load(
    "Projects/Flappy Bird/assets/pipe-green.png").convert()
pipe2x = pygame.transform.scale2x(pipe)
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)
pipe_list = []
pipe_height = [210, 250, 300, 350, 400]
flap_sound = pygame.mixer.Sound('Projects/Flappy Bird/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('Projects/Flappy Bird/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Projects/Flappy Bird/sound/sfx_point.wav')
score_sound_countdown = 100
game_over_surface = pygame.transform.scale2x(
    pygame.image.load('Projects/Flappy Bird/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -5.5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird2x_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    # xet background va vi tri background
    screen.blit(background2x, (0, 0))
    if game_active == True:
        rotated_bird = rotate_bird(bird2x)
        bird_movement += gravity
        bird2x_rect.centery += bird_movement
        screen.blit(rotated_bird, bird2x_rect)
        game_active = check_collision(pipe_list)
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display("main game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game over")
    # xet vi tri va cho san lui ve phia ben trai
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
