# Schritt 1: Module importen
import pygame
from enum import Enum
import random
import time

# Schritt 2: class Direction erstellen und Enum erben lassen
import pygame.display


class Direction(Enum):
    HOCH = 1
    RUNTER = 2
    RECHTS = 3
    LINKS = 4

# Schritt 3: FensterVariablen festlegen


Geschwindigkeit = 10

x = 1250
y = 625


scale = 20

# Schritt 4: Pygame initialisieren

pygame.init()
pygame.display.set_caption("SpySnake")
Fenster = pygame.display.set_mode((x, y))
FPS = pygame.time.Clock()


Schlangen_Position = [250, 250]
Schlangen_Körper = [[250, 250],
                    [240, 250],
                    [230, 250]]

Futter_Position = [10, 10]
Futter_Position[0] = random.randint(5, (x - 2) // scale) * scale
Futter_Position[1] = random.randint(5, (y - 2) // scale) * scale

score = 0


# Schritt 5: Game_Loop definieren und unsere funktionen Benennen und definieren


def Fenster_zeichnen():
    Fenster.fill(pygame.Color(0, 255, 100))
    for Körper in Schlangen_Körper:
        pygame.draw.circle(Fenster, pygame.Color(136, 23, 152), (Körper[0], Körper[1]), scale / 2)
    pygame.draw.rect(Fenster, pygame.Color(255, 0, 0),
                     pygame.Rect(Futter_Position[0] - scale / 2, Futter_Position[1] - scale / 2, scale, scale))


def HUD():
    font = pygame.font.SysFont('Arial', scale * 2)
    render = font.render(f'Score: {score}', True, pygame.Color(0, 0, 0))
    rect = render.get_rect()
    Fenster.blit(render, rect)


def Schlangen_Steuerung(direction):
    neue_direction = direction
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit(0)
        if event.key == pygame.K_UP and direction != Direction.RUNTER:
            neue_direction = Direction.HOCH
        if event.key == pygame.K_DOWN and direction != Direction.HOCH:
            neue_direction = Direction.RUNTER
        if event.key == pygame.K_RIGHT and direction != Direction.LINKS:
            neue_direction = Direction.RECHTS
        if event.key == pygame.K_LEFT and direction != Direction.RECHTS:
            neue_direction = Direction.LINKS
    return neue_direction


def Schlange_bewegen(direction):
    if direction == Direction.HOCH:
        Schlangen_Position[1] -= scale
    if direction == Direction.RUNTER:
        Schlangen_Position[1] += scale
    if direction == Direction.LINKS:
        Schlangen_Position[0] -= scale
    if direction == Direction.RECHTS:
        Schlangen_Position[0] += scale
    Schlangen_Körper.insert(0, list(Schlangen_Position))


def Futter_generieren():
    Futter_Position[0] = random.randint(5, (x - 2) // scale) * scale
    Futter_Position[1] = random.randint(5, (y - 2) // scale) * scale


def Futter_Fressen():
    global score
    if abs(Schlangen_Position[0] - Futter_Position[0]) < 20 and abs(Schlangen_Position[1] - Futter_Position[1]) < 20:
        score += 10
        Futter_generieren()
    else:
        Schlangen_Körper.pop()


def Game_Over_Nachricht():
    font = pygame.font.SysFont('Arial', scale * 3)
    render = font.render(f'Score: {score}', True, pygame.Color(0, 0, 0))
    rect = render.get_rect()
    rect.midtop = (x / 2, y / 2)
    Fenster.blit(render, rect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    exit(0)


def Game_Over():
    if Schlangen_Position[0] < 0 or Schlangen_Position[0] > x - 10:
        Game_Over_Nachricht()
    if Schlangen_Position[1] < 0 or Schlangen_Position[1] > y - 10:
        Game_Over_Nachricht()
    for Körper in Schlangen_Körper[1:]:
        if Schlangen_Position[0] == Körper[0] and Schlangen_Position[1] == Körper[1]:
            Game_Over_Nachricht()


def Game_Loop():
    direction = Direction.RECHTS
    while True:
        Fenster_zeichnen()
        HUD()
        direction = Schlangen_Steuerung(direction)
        Schlange_bewegen(direction)
        Futter_Fressen()
        Game_Over()
        pygame.display.update()
        FPS.tick(Geschwindigkeit)
        time.sleep(0.1)

# Schritt 6: Main_Loop initialisieren und


if __name__ == "__main__":
    Game_Loop()
