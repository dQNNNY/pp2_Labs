import pygame, sys, random, time
import psycopg2

# Game settings
frame_size_x = 1380
frame_size_y = 840
square_size = 60

# Initialize pygame and mixer for sounds
pygame.init()
pygame.mixer.init()

# Game window settings
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

fps_controller = pygame.time.Clock()

# Connect to database
conn = psycopg2.connect(
    dbname="snakegame",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Ask for username
username = input("Enter your username: ")

cur.execute("SELECT * FROM users WHERE username = %s", (username,))
user_exists = cur.fetchone()

if not user_exists:
    cur.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    cur.execute("INSERT INTO user_score (username, score, level) VALUES (%s, %s, %s)", (username, 0, 1))
    conn.commit()
    level = 1
    score = 0
else:
    cur.execute("SELECT score, level FROM user_score WHERE username = %s", (username,))
    score, level = cur.fetchone()

# Get level settings (walls and speed)
def get_level_settings(level):
    if level == 1:
        return 4, []  # Speed 4, no walls
    elif level == 2:
        return 6, [[600, 300, 180, 60]]  # Speed 6, one wall
    elif level == 3:
        return 8, [[300, 300, 780, 60], [300, 500, 780, 60]]  # Speed 8, two walls
    return 4, []  # Default speed and no walls

# Initialize game variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, direction, food_weight, food_timer, speed, walls
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_weight = random.randint(1, 5)
    food_spawn = True
    speed, walls = get_level_settings(level)
    food_timer = time.time()

# Show score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f"Score: {score}  Speed: {speed}  Level: {level}", True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Start game
init_vars()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save game state before quitting
            cur.execute("UPDATE user_score SET score = %s, level = %s WHERE username = %s",
                        (score, level, username))
            conn.commit()
            print(f"Game over! Your score: {score} and level: {level} have been saved.")
            pygame.quit()
            cur.close()
            conn.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == ord("w")) and direction != "DOWN":
                direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == ord("s")) and direction != "UP":
                direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == ord("a")) and direction != "RIGHT":
                direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == ord("d")) and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_p:
                paused = True
                # Save game state during pause
                cur.execute("UPDATE user_score SET score = %s, level = %s WHERE username = %s",
                            (score, level, username))
                conn.commit()
                print("Game paused. Press P again to resume.")
                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:
                            paused = False

    # Move
    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size

    # Wrap around screen
    head_pos[0] %= frame_size_x
    head_pos[1] %= frame_size_y

    # Update snake
    snake_body.insert(0, list(head_pos))

    if head_pos == food_pos:
        score += food_weight
        if score >= level * 10:  # Level up condition
            level += 1
            init_vars()
        food_spawn = False
    else:
        snake_body.pop()

    # Respawn food
    if not food_spawn or (time.time() - food_timer > 5):
        food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                    random.randrange(1, (frame_size_y // square_size)) * square_size]
        food_weight = random.randint(1, 5)
        food_spawn = True
        food_timer = time.time()

    # Draw everything
    game_window.fill(black)

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0] + 2, pos[1] + 2, square_size - 4, square_size - 4))

    # Draw food
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], square_size, square_size))

    # Draw walls
    for wall in walls:
        pygame.draw.rect(game_window, blue, pygame.Rect(*wall))

    # Wall collision
    for wall in walls:
        wall_rect = pygame.Rect(*wall)
        if wall_rect.collidepoint(head_pos[0], head_pos[1]):
            init_vars()

    # Self collision
    for block in snake_body[1:]:
        if head_pos == block:
            init_vars()

    # Show score
    show_score(1, white, 'courier', 20)
    pygame.display.update()

    # Control game speed
    fps_controller.tick(speed)
