import pygame
import os

pygame.init()
pygame.mixer.init()

BASE_PATH = r"C:\Users\Daniyar\Desktop\labs\lab_7\task2"
MUSIC_PATH = os.path.join(BASE_PATH, "music")
BUTTONS_PATH = os.path.join(BASE_PATH, "knopki")

tracks = [
    os.path.join(MUSIC_PATH, "Qurmash Makhan - Жан сырым (Аяулым).mp3"),
    os.path.join(MUSIC_PATH, "yenlik-men-dep-ojla-cover_(muzzonas.ru).mp3"),
    os.path.join(MUSIC_PATH, "Мирас Жугунусов - Janym.mp3")
]

current = 0

if os.path.exists(tracks[current]):
    pygame.mixer.music.load(tracks[current])
    pygame.mixer.music.play()

display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music Player")
back_color = (169, 171, 170)

def load_image(filename):
    path = os.path.join(BUTTONS_PATH, filename)
    return pygame.image.load(path) if os.path.exists(path) else pygame.Surface((50, 50))

image_back = load_image("back 1.png")
image_next = load_image("back 2.png")
image_pause = load_image("pause 1.png")
image_play = load_image("play 1.png")

back = image_back.get_rect(center=(250, 300))
pause = image_pause.get_rect(center=(350, 300))
play = image_play.get_rect(center=(450, 300))
next = image_next.get_rect(center=(550, 300))

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play.collidepoint(event.pos):
                pygame.mixer.music.unpause()
            elif pause.collidepoint(event.pos):
                pygame.mixer.music.pause()
            elif next.collidepoint(event.pos):
                current = (current + 1) % len(tracks)
                if os.path.exists(tracks[current]):
                    pygame.mixer.music.load(tracks[current])
                    pygame.mixer.music.play()
            elif back.collidepoint(event.pos):
                current = (current - 1) % len(tracks)
                if os.path.exists(tracks[current]):
                    pygame.mixer.music.load(tracks[current])
                    pygame.mixer.music.play()

    display.fill(back_color)
    display.blit(image_back, back)
    display.blit(image_pause, pause)
    display.blit(image_play, play)
    display.blit(image_next, next)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
