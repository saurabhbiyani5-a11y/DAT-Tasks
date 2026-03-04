import pygame
import random
import math

pygame.init()

# ================= SETTINGS =================
WIDTH, HEIGHT = 1100, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Titanic Cruise: Sea Adventure")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)

# COLORS
SKY_TOP = (10, 20, 40)  # Deep twilight
SKY_BOTTOM = (44, 62, 80)
SEA_DEEP = (10, 30, 60)
SEA_SURFACE = (20, 80, 120)
WHITE = (240, 240, 240)
BRASS = (184, 134, 11)
SMOKE_GRAY = (80, 80, 80)


# ================= CLASSES =================
class SmokeParticle:
    """ Engine smoke from funnels """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = random.uniform(-1, -2)
        self.vel_x = random.uniform(-0.5, 0.5)
        self.size = random.randint(5, 15)
        self.life = 255

    def update(self):
        self.y += self.vel_y
        self.x += self.vel_x
        self.life -= 3
        self.size += 0.2

    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (SMOKE_GRAY[0], SMOKE_GRAY[1], SMOKE_GRAY[2], self.life),
                               (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (self.x - self.size, self.y - self.size))


class Fish:
    def __init__(self):
        self.reset()

    def reset(self):
        self.size = random.randint(10, 25)
        # Deeper fish are darker
        self.depth = random.randint(480, 620)
        brightness = int((self.depth / HEIGHT) * 255)
        self.color = (random.randint(0, 100), brightness, random.randint(150, 255))
        self.x = random.randint(-100, WIDTH + 100)
        self.speed = random.uniform(0.5, 2.5)
        self.dir = random.choice([-1, 1])

    def move(self):
        self.x += self.speed * self.dir
        if self.x > WIDTH + 100 or self.x < -100:
            self.dir *= -1

    def draw(self):
        # Subtle swimming oscillation
        y_osc = math.sin(pygame.time.get_ticks() * 0.005 + self.x) * 5
        pygame.draw.ellipse(screen, self.color, (self.x, self.depth + y_osc, self.size, self.size // 2))
        # Tail
        tail_x = self.x + self.size if self.dir == -1 else self.x - 5
        pygame.draw.polygon(screen, self.color, [(tail_x, self.depth + y_osc), (tail_x, self.depth + 10 + y_osc),
                                                 (self.x + self.size // 2, self.depth + 5 + y_osc)])


# ================= INITIALIZATION =================
fishes = [Fish() for _ in range(25)]  # Many more fish
smoke_particles = []
boat_x = 300
wave_time = 0
arrived = False
boat_direction = 1

# ================= MAIN LOOP =================
running = True
while running:
    # 1. ATMOSPHERIC BACKGROUND
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        if y < 430:  # Sky
            col = [SKY_TOP[i] * (1 - ratio) + SKY_BOTTOM[i] * ratio for i in range(3)]
        else:  # Deep Sea
            col = [SEA_SURFACE[i] * (1 - ratio) + SEA_DEEP[i] * ratio for i in range(3)]
        pygame.draw.line(screen, col, (0, y), (WIDTH, y))

    # 2. MOUNTAIN SILHOUETTES
    pygame.draw.polygon(screen, (15, 25, 35), [(0, 430), (300, 200), (500, 430), (800, 150), (1100, 430)])

    # 3. SHIP LOGIC
    keys = pygame.key.get_pressed()
    moving = False
    if not arrived:
        if keys[pygame.K_RIGHT]:
            boat_x += 2.5  # Larger ships move slower/heavier
            boat_direction = 1
            moving = True
        if keys[pygame.K_LEFT]:
            boat_x -= 2.5
            boat_direction = -1
            moving = True

    # 4. DRAW TITANIC SHIP
    wave_time += 0.03
    ship_y = 410 + math.sin(wave_time) * 5

    # Smoke generation from 4 funnels
    if moving and random.random() > 0.5:
        for i in range(4):
            smoke_particles.append(SmokeParticle(boat_x + (i * 40 - 60) * boat_direction, ship_y - 60))

    # Ship Body Rendering
    # Surface for the ship to allow flipping
    ship_surf = pygame.Surface((300, 200), pygame.SRCALPHA)

    # Funnels (The iconic 4)
    for i in range(4):
        f_x = 80 + (i * 45)
        pygame.draw.rect(ship_surf, (200, 140, 0), (f_x, 30, 25, 60))  # Yellow/Buff
        pygame.draw.rect(ship_surf, (20, 20, 20), (f_x, 30, 25, 15))  # Black top

    # Hull Upper (White)
    pygame.draw.rect(ship_surf, WHITE, (50, 90, 220, 40), border_top_left_radius=15, border_top_right_radius=15)
    # Hull Lower (Black)
    pygame.draw.polygon(ship_surf, (15, 15, 15), [(30, 130), (270, 130), (250, 180), (50, 180)])
    # Portholes (Glowing)
    for px in range(70, 240, 20):
        pygame.draw.circle(ship_surf, (255, 255, 150), (px, 110), 3)
        pygame.draw.circle(ship_surf, (255, 255, 150), (px, 145), 3)

    if boat_direction == -1: ship_surf = pygame.transform.flip(ship_surf, True, False)
    screen.blit(ship_surf, (boat_x - 150, ship_y - 100))

    # 5. WATER WAVES (Overlapping Ship)
    for i in range(2):
        layer_y = 440 + (i * 50)
        points = [(0, HEIGHT)]
        for x in range(0, WIDTH + 20, 20):
            y = layer_y + math.sin(x * 0.008 + wave_time + i) * 12
            points.append((x, y))
        points.append((WIDTH, HEIGHT))
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(s, (20, 100, 180, 150), points)
        screen.blit(s, (0, 0))

    # 6. SMOKE & FISH
    for p in smoke_particles[:]:
        p.update()
        p.draw(screen)
        if p.life <= 0: smoke_particles.remove(p)

    for f in fishes:
        f.move()
        f.draw()

    # 7. ARRIVAL LOGIC
    if boat_x > WIDTH - 180 or boat_x < 180:
        arrived = True
        txt = font.render("DOCKED AT HARBOR", True, WHITE)
        screen.blit(txt, (WIDTH // 2 - 120, 100))
        sub = font.render("Press 'C' to set sail again", True, BRASS)
        screen.blit(sub, (WIDTH // 2 - 140, 140))

    # 8. EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and arrived:
                boat_direction *= -1
                arrived = False
                boat_x += 50 * boat_direction

    pygame.display.flip()
    clock.tick(60)

pygame.quit()