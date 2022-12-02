# Imports
import pygame
import time
from aco import *


# Définition des couleurs utilisées par la suite
ANT = (0, 0, 0)
LEAD = (0, 0, 255)
BACKGROUND = (255, 255, 255)
RESSOURCE = (255, 0, 0)
PHEROMONES = (0, 255, 0)
COLONY = (255, 255, 0)
WALL = (130, 100, 20)

# Paramètres
scale = 5

# Initialisation de pygame
pygame.init()
pygame.display.set_caption("ACO")
screen = pygame.display.set_mode([int(ter_size * scale), int(ter_size * scale)])
clock = pygame.time.Clock()
    

# Procédure réalisant l'affichage dans la fenêtre
def DrawField():
    screen.fill(BACKGROUND)
    for i in range(ter_size):
        for j in range(ter_size):
            if matrix[i][j] == "spawn":
                DrawPoint(COLONY, 255, i, j)

            elif matrix[i][j] == "ressource":
                DrawPoint(RESSOURCE, 255, i, j)

            elif matrix[i][j] == "obstacle":
                DrawPoint(WALL, 150, i, j)

            else:
                if matrix[i][j] > 1:    # Si le niveau de phéromone est plus élevé que le niveau par défaut
                    DrawPoint(PHEROMONES, 100, i, j)

# Procédure réalisant l'affichage des fourmis
def DrawAnts():
    for n in ants:
        if (n.is_leader):
            DrawPoint(LEAD, 120, n.x, n.y)
        else:
            DrawPoint(ANT, 120, n.x, n.y)

# Procédure dessinant un point à l'écran
def DrawPoint(color, alpha, x, y):
    s = pygame.Surface((scale, scale))  # the size of your rect
    s.set_alpha(alpha)                # alpha level
    s.fill(color)           # this fills the entire surface
    screen.blit(s, (x * scale, y * scale))    # (0,0) are the top-left coordinates
    return (x*scale, y*scale)

def Update():

    DrawField()
    DrawAnts()
    UpdateACO()
    pygame.display.flip()
    clock.tick()

def main():
    # Initilisation du terrain
    InitTerrain(ter_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        Update()
                
    pygame.quit()
    

main()
