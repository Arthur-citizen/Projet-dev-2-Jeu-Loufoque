import math
import pygame
import random
questions_rand = ["Pourquoi le ciel est bleu ?", "Pourquoi la Terre est-elle ronde ?", "Où est le Nord ?", "regarde la porte."]
réponse_rand = ["Parce qu'il serai rouge sinon", "Parce que tu crois qu'elle est ronde ?? Ferme le jeu si tu penses que oui!!!"]

def random_range(min=0, max=10):
    return random.uniform(min, max)
    
def rand_list(list):
    return random.choice(list)



# par la même occasion cela importe pygame.locals dans l'espace de nom de Pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
coordonee_block = [[30, 30],
            [100, 30],
            [170, 30],
            [240, 30],
            ]
liste_color = ["red", "blue", "green", "purple"]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # pygame.draw.circle(screen, "red", player_pos, 40)
    for position in coordonee_block:
            pygame.draw.rect(screen, random.choice(liste_color), pygame.Rect(position, (60, 60)),  2, 3)


    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()