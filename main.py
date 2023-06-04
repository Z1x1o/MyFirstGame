import time
import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

BACKGROUND_COLOR = "#134892"
PLATFORM_COLOR = "#996779"
COLOR = "#000000"

MOVE_SPEED = 6
WIDTH = 22
HEIGHT = 32
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
JUMP_POWER = 10
GRAVITY = 3

pygame.init()
pygame.font.init()

class ParticleManager:
    def __init__(self, filename=None):
        self.particles = []
        self.radius = 10

    def add_particles(self, x, y, color):
        self.particles.append([x, y, self.radius, -1, 0, color])
        self.particles.append([x, y, self.radius, -1, 1, color])
        self.particles.append([x, y, self.radius, -1, -1, color])
        self.particles.append([x, y, self.radius, 0, -1, color])
        self.particles.append([x, y, self.radius, 0, 1, color])
        self.particles.append([x, y, self.radius, 1, -1, color])
        self.particles.append([x, y, self.radius, 1, 0, color])
        self.particles.append([x, y, self.radius, 1, 1, color])

    def emit(self, screen):
        for p in self.particles:
            p[0] += p[3]
            p[1] += p[4]
            p[2] -= 0.2
            if p[2] <= 0:
                self.particles.remove(p)
            else:
                pygame.draw.circle(screen, p[5],
                                   (int(p[0]), int(p[1])), int(p[2]))

    def clear(self):
        self.particles.clear()

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.yvel = 0
        self.onGround = False
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.count_jump = 0

    def update(self, platforms):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= MOVE_SPEED
            if sprite.spritecollide(self, platforms, False):
                self.rect.x += MOVE_SPEED
        elif keys[K_d]:
            self.rect.x += MOVE_SPEED
            if sprite.spritecollide(self, platforms, False):
                self.rect.x -= MOVE_SPEED

        if self.onGround and keys[K_SPACE]:
            self.onGround = False
            self.count_jump = 20

        if not self.onGround and self.count_jump > 0:
            self.rect.y -= JUMP_POWER
            self.count_jump -= 1
            while sprite.spritecollide(self, platforms, False):
                self.rect.y += GRAVITY
                self.count_jump = 0

        self.rect.y += GRAVITY
        if sprite.spritecollide(self, platforms, False):
            self.rect.y -= GRAVITY
            self.onGround = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Platform(sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    display.set_caption("ИГРА")
    screen = display.set_mode(DISPLAY)
    font_score = pygame.font.SysFont("Arial", 30, bold=True)
    font_live = pygame.font.SysFont("Arial", 30, bold=True)
    particles = ParticleManager()
    level = [
        "-------------------------",
        "-                       -",
        "-              -----    -",
        "--      +               -",
        "-                 +     -",
        "-     ---               -",
        "-           +           -",
        "-         ---           -",
        "-                   --- -",
        "-     +              +  -",
        "-              +        -",
        "-      ---              -",
        "-  +                    -",
        "-----        -------    -",
        "-                       -",
        "-          +            -",
        "-                   --  -",
        "-  +                    -",
        "-    -------     +      -",
        "-------------------------"]

    hero = Player(50, 50)
    platforms = sprite.Group()
    score = 0
    live = 3
    red = sprite.Group()
    x, y = 0, 0
    for row in level:
        for col in row:
            if col == "/":
                pf =Platform(x, y, "red")
                red.add(pf)
            if col == "-":
                pf = Platform(x, y, PLATFORM_COLOR)
                platforms.add(pf)
            if col == "+":
                pf = Platform(x, y, "red")
                red.add(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    clock = time.Clock()
    a = pygame.USEREVENT + 1
    parcticles = []
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == a:
                for p in parcticles:
                    parcticles(*p[0], "red")
                    p[1] -= 1
                    if p[1] == 0:
                        parcticles.remove(p)

        hero.update(platforms)
        screen.fill(BACKGROUND_COLOR)
        platforms.draw(screen)
        red.draw(screen)
        particles.emit(screen)
        hero.draw(screen)

        collide = sprite.spritecollide(hero, red, True)
        for c in collide:
            print("red")
            score += 1

            particles.add_particles(*c.rect.center, "red")
            parcticles.append([c.rect.center, 5])

        score_img = font_score.render(f"Счёт: {score}", True, "black")
        screen.blit(score_img, (30, 0))

        if score > 0 and score % 10 == 0:
            level = 0

        live_img = font_live.render(f"Жизнь: {live}", True, "black")
        screen.blit(live_img, (655, 0))

        if live > 0 and live % 3 == 0:
            level = 0

        display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

