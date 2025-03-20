from pygame import *
import random

# Ініціалізація Pygame
init()

bgmusic = "bgg.ogg"
bonusmusic = "win.ogg"
ffalse = "boon.ogg"

#Ініціалізація
mixer.init()

mixer.music.load(bgmusic)
mixer.music.play(-1)


# Параметри вікна
WIDTH, HEIGHT = 500, 500
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Доджер")

# Колір
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Шрифт
font = font.Font(None, 36)
font1 = pygame.font.Font(None, 80)

#Тексти
win = font1.render('You Win!', True, (255, 255, 255))
lose = font1.render('You Lose!', True, (180, 0, 0))


# Гравець
player_size = 35
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 0.2

# Перешкоди
obstacle_size = 40
obstacle_speed = 0.1
obstacles = []

# Бонуси
bonus_size = 30
bonus_speed = 0.3
bonuses = []

# Таймери
spawn_timer = 0
spawn_interval = 1500  # Кожні 50 кадрів
bonus_timer = 0
bonus_interval = 1000  # Кожні 100 кадрів

# Очки
score = 0
bonus_goal = 25

# Головний цикл гри
running = True
while running:
    screen.fill(WHITE)
    
    for e in event.get():
        if e.type == QUIT:
            running = False
    
    keys = key.get_pressed()
    if keys[K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    
    # Створення перешкод
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        obstacle_x = random.randint(0, WIDTH - obstacle_size)
        obstacles.append([obstacle_x, 0])
    
    # Створення бонусів
    bonus_timer += 1
    if bonus_timer >= bonus_interval:
        bonus_timer = 0
        bonus_x = random.randint(0, WIDTH - bonus_size)
        bonuses.append([bonus_x, 0])
    
    # Рух перешкод
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
    
    # Рух бонусів
    for bonus in bonuses:
        bonus[1] += bonus_speed
    
    # Перевірка на зіткнення з перешкодами
    for obstacle in obstacles:
        if (player_x < obstacle[0] < player_x + player_size or player_x < obstacle[0] + obstacle_size < player_x + player_size) and player_y < obstacle[1] + obstacle_size < player_y + player_size:
            mixer.Sound(ffalse).play()
            running = False
            
    
    # Перевірка на підбір бонусів
    for bonus in bonuses[:]:
        if (player_x < bonus[0] < player_x + player_size or player_x < bonus[0] + bonus_size < player_x + player_size) and player_y < bonus[1] + bonus_size < player_y + player_size:
            bonuses.remove(bonus)
            score += 1
            mixer.Sound(bonusmusic).play()
            
    
    # Перевірка на перемогу
    if score >= bonus_goal:
        print("Ви виграли!")
        screen.blit(win, (100,100))
        running = False
    
    # Малювання
    draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    for obstacle in obstacles:
        draw.rect(screen, BLUE, (obstacle[0], obstacle[1], obstacle_size, obstacle_size))
    for bonus in bonuses:
        draw.rect(screen, GREEN, (bonus[0], bonus[1], bonus_size, bonus_size))
    
    # Відображення рахунку бонусів
    score_text = font.render(f"Бонуси: {score}/{bonus_goal}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    display.update()
    
quit()