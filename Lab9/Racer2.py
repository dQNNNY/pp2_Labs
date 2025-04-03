import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Установка рабочего каталога
os.chdir(os.path.dirname(__file__))


car_image_path = "car.png"        
bg_image_path = "background.png"  
sound_path = "coin_sound.wav"     


coin_sound = pygame.mixer.Sound(sound_path)


WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")


WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)

background = pygame.image.load(bg_image_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


car_image = pygame.image.load(car_image_path)
car_width, car_height = 50, 100
car_image = pygame.transform.scale(car_image, (car_width, car_height))

car = pygame.Rect(WIDTH // 2 - car_width // 2, HEIGHT - 150, car_width, car_height)

# Параметры монет
coin_size = 30
coins = []
coin_spawn_timer = 0
coin_spawn_interval = 1000

score = 0
font = pygame.font.Font(None, 36)

speed = 7

speed_increase_threshold = 5

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление машиной
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car.left > 0:
        car.x -= speed
    if keys[pygame.K_RIGHT] and car.right < WIDTH:
        car.x += speed

    # Спавн монет
    coin_spawn_timer += clock.get_time()
    if coin_spawn_timer >= coin_spawn_interval:
        coin_x = random.randint(0, WIDTH - coin_size)
        # Рандомное значение для "веса" монеты (количество очков)
        coin_weight = random.randint(1, 3)  # Вес от 1 до 3
        coins.append({"rect": pygame.Rect(coin_x, -coin_size, coin_size, coin_size), "weight": coin_weight})
        coin_spawn_timer = 0

    for coin in coins[:]:
        coin["rect"].y += speed
        if coin["rect"].colliderect(car):  # Проверка столкновения машины с монетой
            score += coin["weight"]
            coin_sound.play()
            coins.remove(coin)
        elif coin["rect"].y > HEIGHT:
            coins.remove(coin)

    if score // speed_increase_threshold > 0:
        speed = 7 + (score // speed_increase_threshold)  # Увеличение скорости на основе количества очков

    screen.blit(background, (0, 0))

    screen.blit(car_image, (car.x, car.y))

    for coin in coins:
        pygame.draw.ellipse(screen, YELLOW, coin["rect"])

    # Отображение счёта в правом верхнем углу
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
