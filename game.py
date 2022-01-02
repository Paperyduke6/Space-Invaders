import pygame
import math
import random
from pygame import mixer

# using pygame
pygame.init()
# set screen size
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('spaceship.png')
# Application icon
pygame.display.set_icon(icon)
# Application Caption
pygame.display.set_caption('Space Invaders')
check = True
# Score Calculation
score = 0
textx = 10
texty = 10
font = pygame.font.Font('freesansbold.ttf', 32)
# Background Music
mixer.music.load('01._You_Say_Run.mp3')
mixer.music.play(-1)
# Game over
new_font = pygame.font.Font('freesansbold.ttf', 72)
# player
playerimg = pygame.image.load('spaceship (1).png')
playerx = 370
playery = 460
change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemy_xchange = []
enemy_ychange = 40
no = 6
for i in range(no):
    enemyimg.append(pygame.image.load('ufo.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemy_xchange.append(0.8)

# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 460
bullet_xchange = 0
bullet_ychange = 0.8
bullet_state = 'ready'

background = pygame.image.load('18761.jpg')


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))


def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 30:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        return True
    else:
        return False


def show_score(x, y):
    score_value = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def game_over():
    end_text = new_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(end_text, (200, 250))


# Game Loop
while check:
    # RGB colours
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check = False
        # Keyboard Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -1
            if event.key == pygame.K_RIGHT:
                change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0.0
    playerx += change
    # Player boundary
    if playerx < 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # Enemy Movement
    for i in range(no):
        if enemyy[i] >= 400:
            for j in range(no):
                enemyy[j] = 1000
            game_over()
            break
        enemyx[i] += enemy_xchange[i]
        if enemyx[i] < 0:
            enemy_xchange[i] = 0.6
            enemyy[i] += enemy_ychange
        elif enemyx[i] >= 736:
            enemy_xchange[i] = -0.6
            enemyy[i] += enemy_ychange

            # Collision
        collide = collision(enemyx[i], enemyy[i], bulletx, bullety)
        if collide:
            bullety = 460
            score += 1
            bullet_state = "ready"
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)

    # bullet Movement
    if bullety < 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == 'fire':
        bullet(bulletx, bullety)
        bullety -= bullet_ychange

    show_score(textx, texty)
    player(playerx, playery)
    pygame.display.update()
