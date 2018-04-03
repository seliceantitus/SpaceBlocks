import pygame
import random
from player import Player
from blocks import Block
from bullets import Bullet
from randomizer import Randomizer
from particles import Particle
from powerup import Powerup

pygame.init()

# Window and main game variables
width = 400
height = 720
screen = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(0)
done = False
rand = Randomizer()

# Background image
background = pygame.image.load("img/bg.gif");
background = pygame.transform.scale(background, (width, height))
background_rect = background.get_rect()

# Score area
font = pygame.font.SysFont('Calibri', 30, True, False)
font_color = pygame.Color('white')
score = 0
score_width = 380
score_height = 50
score_area = pygame.Surface((score_width, score_height))
score_area_shadow = pygame.Surface((score_width + 8, score_height - 10))
score_color = (80, 30, 145)
score_shadow_color = (130, 80, 200)
score_rect = score_area.get_rect()
score_shadow_rect = score_area_shadow.get_rect()
score_rect.x = 10
score_rect.y = 660
score_shadow_rect.x = 6
score_shadow_rect.y = 675
score_text_surface = font.render("Score : 0", True, font_color)
score_text_rect = score_text_surface.get_rect(center = score_rect.center)

# Time variables
clock = pygame.time.Clock()
timestamp = 0
time = 0

# Bullets variables and sprite group
shoot_speed = 10
shoot_interval = 1000 / shoot_speed
last_shot = 0
bullet_speed = 8
bullet_power = 100
bullet_width = 40
bullet_height = 20
bullets_group = pygame.sprite.Group()
bullet_boost = -1

# Player object and sprite group
player = Player(50, 50)
player_group = pygame.sprite.Group()
player_group.add(player)

# Block variables and sprite group
scene_speed = 2
block_width = 80
block_height = 80
block_x_increment = 80
block_y_increment = 0
last_block_spawn = 0
block_spawn_interval = 4
first_block_spawn = True

blocks_group = pygame.sprite.Group()

# Particle group
particle_group = pygame.sprite.Group()

# Powerup group
powerup_group = pygame.sprite.Group()
powerup_width = 40
powerup_height = 40
power_up_spawn_interval = 7
last_powerup_spawn = 0
powerup_enable = 0
powerup_duration = 7
active_powerups = []
powerup_active = False

def set_player_coord(x_coord):
    # Left border limit
    if (x_coord <= 5):
        player_x = 0
        return player_x

    # Right border limit
    if (x_coord >= width - 70):
        player_x = width - 70
        return player_x

    # If not on the edges return the current x coordinate
    return x_coord

def shoot(time, last_shot, shoot_interval):
    if (time - last_shot >= shoot_interval):
        if bullet_boost != 2:
                bullet = Bullet(bullet_boost, bullet_width, bullet_height, player.get_x() + 15, 600 - 75, 0)
                bullets_group.add(bullet)
        else:
                bullet_center = Bullet(bullet_boost, bullet_width, bullet_height, player.get_x() + 15, 600 - 75, 0)
                bullet_left = Bullet(bullet_boost, bullet_width, bullet_height, player.get_x() + 10, 600 - 75, 6)
                bullet_right = Bullet(bullet_boost, bullet_width, bullet_height, player.get_x() + 20, 600 - 75, -6)
                bullets_group.add(bullet_center)
                bullets_group.add(bullet_left)
                bullets_group.add(bullet_right)
        return True
    else:
        return False
        
def create_particles(x, y, color):
    count = random.randrange(20, 30, 1)
    numbers = range(-5, -1) + range(1, 5)
    for i in range(0, count):
        particle_group.add(Particle(x + 40, y + 40, random.choice(numbers), random.choice(numbers), random.randint(3,8), color))

def create_blocks():
    global blocks_group 

    colors = rand.get_random_color(5)
    values = rand.get_random_block_numbers(time)
    x = 0
    y = -80
    for i in range(0, 5):
        block = Block(colors[i], block_width, block_height, x, y, values[i])
        x += block_x_increment
        y += block_y_increment
        blocks_group.add(block)

def get_block_pos():
    global blocks_group

    positions = range(0, width - powerup_width)
    x = random.choice(positions)
    if len(blocks_group) > 0:
        sprites = blocks_group.sprites()
        y = sprites[0].get_y()
        if y <= 60:
            y = -200
        else:
            y = -60
        return (x, y)
    else:
        y = -170
        return (x, y)

def create_powerup():
    ids = [0, 1, 2]
    powerup_id = random.choice(ids)
    x_set = range(0, width - powerup_width)
    y_set = range(-110, -90)
    # (x, y) = (random.choice(x_set), random.choice(y_set))
    (x, y) = get_block_pos()
    powerup = Powerup(powerup_id, powerup_width, powerup_height, x, y)
    powerup_group.add(powerup)

def check_powerups(time):
    global active_powerups

    for pw in active_powerups:
        if (time - pw.get_active() >= (powerup_duration * 1000)):
            disable_powerup(pw)

def enable_powerup(powerup, time):
    global shoot_speed
    global shoot_interval
    global bullet_power
    global bullet_boost
    global powerup_active

    powerup.set_active(time)
    pw_id = powerup.get_id()

    if (pw_id == 0):
        shoot_speed += powerup.get_speed_increase()
        shoot_interval = 1000 / shoot_speed
    elif (pw_id == 1):
        bullet_power *= powerup.get_power_increase()
    elif (pw_id == 2):
        shoot_speed -= powerup.get_speed_decrease()
        shoot_interval = 1000 / shoot_speed
        bullet_power *= (powerup.get_power_increase() / 2)

    bullet_boost = pw_id
    powerup_active = True

def disable_powerup(powerup):
    global shoot_speed
    global shoot_interval
    global bullet_power
    global active_powerups
    global bullet_boost
    global powerup_active

    pw_id = powerup.get_id()
    if (pw_id == 0):
        shoot_speed -= powerup.get_speed_increase()
        shoot_interval = 1000 / shoot_speed
    elif (pw_id == 1):
        bullet_power /= powerup.get_power_increase()
    elif (pw_id == 2):
        shoot_speed += powerup.get_speed_decrease()
        shoot_interval = 1000 / shoot_speed
        bullet_power /= (powerup.get_power_increase() / 2)

    bullet_boost = -1
    active_powerups.remove(powerup)
    powerup.kill()
    powerup_active = False

def update_score():
    score_area.fill(score_color)
    score_area_shadow.fill(score_shadow_color)

    score_text_surface = font.render("Score : " + str(score), True, font_color)
    score_text_rect = score_text_surface.get_rect(center = score_rect.center)

    pygame.draw.rect(screen, score_shadow_color, score_shadow_rect)
    pygame.draw.rect(screen, score_color, score_rect)
    screen.blit(score_text_surface, score_text_rect)
    # score_area.blit(score_text_surface, score_text_rect)
    # score_area.blit(score_area_shadow, score_shadow_rect)
    

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True

    # Get mouse position 
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    player_x = set_player_coord(mouse_x)

    
    screen.blit(background, background_rect)
    update_score()

    player_group.draw(screen)
    player_group.update(player_x, 600 - 70)

    if len(active_powerups) > 0:
        check_powerups(time)

    if (first_block_spawn):
        create_blocks()
        last_block_spawn = time
        first_block_spawn = False
    elif (time - last_block_spawn >= (block_spawn_interval * 1000)):
        create_blocks()
        last_block_spawn = time

    blocks_group.draw(screen)
    blocks_group.update(0, scene_speed)

    if (time - last_powerup_spawn >= (power_up_spawn_interval * 1000)) and not powerup_active:
        create_powerup()
        last_powerup_spawn = time

    powerup_group.draw(screen)
    powerup_group.update(0, scene_speed)

    if shoot(time, last_shot, shoot_interval):
        last_shot = time

    bullets_group.draw(screen)
    bullets_group.update(0, bullet_speed)

    hit_blocks = pygame.sprite.groupcollide(blocks_group, bullets_group, False, True)
    
    for block in hit_blocks.keys():
        value = block.get_value()
        new_value = value - bullet_power
        score += value - new_value
        if new_value <= 0:
                create_particles(block.get_x(), block.get_y(), block.get_color())
                block.kill()
                score += abs(new_value)
        else:
                block.set_value(new_value)

    if len(particle_group) > 0:
        particle_group.draw(screen)
        particle_group.update()

    hit_powerup = pygame.sprite.groupcollide(powerup_group, player_group, False, False)

    if len(hit_powerup) > 0:
        for powerup in hit_powerup:
            enable_powerup(powerup, time)
            active_powerups.append(powerup)
            powerup_group.remove(powerup)

    if pygame.sprite.groupcollide(player_group, blocks_group, True, False):
        done = True
        print "You died! Your score is : ", score

    pygame.display.flip()

    timestamp = clock.tick(120)
    time += timestamp
    