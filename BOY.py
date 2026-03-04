import pygame
import random

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Great Neighborhood Adventure")
clock = pygame.time.Clock()

# ================= COLORS =================
GRASS_GREEN = (34, 139, 34)
ROAD_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (200, 30, 30)
BROWN = (101, 67, 33)
BLUE = (30, 144, 255)
FRIEND_PURPLE = (150, 50, 250)
SKIN = (255, 224, 189)
BLACK = (20, 20, 20)
YELLOW = (255, 215, 0)

# ================= FONTS =================
font = pygame.font.SysFont("Arial", 22, bold=True)
big_font = pygame.font.SysFont("Arial", 42, bold=True)

# ================= ENTITIES =================
player_pos = pygame.Vector2(440, 520)
friend_pos = pygame.Vector2(440, 520)  # Starts at player, but invisible until met
history = []  # To store player trail for the friend to follow

boy_speed = 4
boy_w, boy_h = 24, 35

# Buildings
road = pygame.Rect(350, 0, 200, HEIGHT)
school = pygame.Rect(360, 10, 180, 70)
home = pygame.Rect(360, HEIGHT - 80, 180, 70)
market = pygame.Rect(50, 250, 150, 100)
friend_house = pygame.Rect(700, 250, 150, 100)

# Cars
car_list = []
lanes = [370, 415, 460, 505]
for i in range(4):
    car_list.append(pygame.Rect(random.choice(lanes), random.randint(-600, 0), 35, 60))


# ================= FUNCTIONS =================
def draw_text(msg, x, y, color=WHITE, center=False):
    img = font.render(msg, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))


def draw_character(pos, color, label=""):
    # Shadow
    pygame.draw.ellipse(screen, (0, 0, 0, 50), (pos.x - 2, pos.y + 25, 28, 10))
    # Head
    pygame.draw.circle(screen, SKIN, (int(pos.x + 12), int(pos.y)), 10)
    # Body
    pygame.draw.rect(screen, color, (int(pos.x), int(pos.y + 10), 24, 15), border_radius=3)
    # Legs
    pygame.draw.rect(screen, BLACK, (int(pos.x + 2), int(pos.y + 25), 8, 10))
    pygame.draw.rect(screen, BLACK, (int(pos.x + 14), int(pos.y + 25), 8, 10))
    if label:
        draw_text(label, pos.x + 12, pos.y - 25, center=True)


def draw_car(rect):
    pygame.draw.rect(screen, RED, rect, border_radius=5)
    pygame.draw.rect(screen, (135, 206, 235), (rect.x + 5, rect.y + 10, 25, 15))
    for dx, dy in [(2, 5), (28, 5), (2, 45), (28, 45)]:
        pygame.draw.circle(screen, BLACK, (rect.x + dx, rect.y + dy), 5)


# ================= GAME STATE =================
# Stages: MEET_FRIEND -> GO_SHOPPING -> GO_SCHOOL -> GO_HOME
stage = "MEET_FRIEND"
has_friend = False
paused = False
timer = 0
message = ""
running = True

# ================= MAIN LOOP =================
while running:
    screen.fill(GRASS_GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and paused and timer <= 0:
            paused = False

    # ---------- MOVEMENT & TRAIL ----------
    if not paused:
        keys = pygame.key.get_pressed()
        old_pos = player_pos.copy()
        if keys[pygame.K_UP] and player_pos.y > 20: player_pos.y -= boy_speed
        if keys[pygame.K_DOWN] and player_pos.y < HEIGHT - 40: player_pos.y += boy_speed
        if keys[pygame.K_LEFT] and player_pos.x > 20: player_pos.x -= boy_speed
        if keys[pygame.K_RIGHT] and player_pos.x < WIDTH - 40: player_pos.x += boy_speed

        # Record history for friend to follow (classic "snake" delay)
        if player_pos != old_pos:
            history.append(player_pos.copy())
            if len(history) > 15:
                friend_pos = history.pop(0)

    # ---------- DRAWING WORLD ----------
    pygame.draw.rect(screen, ROAD_GRAY, road)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, WHITE, (450, y), (450, y + 20), 2)

    # Buildings with Status Highlights
    pygame.draw.rect(screen, (100, 100, 255) if stage == "GO_SCHOOL" else (60, 60, 150), school)
    draw_text("SCHOOL", 450, 45, center=True)

    pygame.draw.rect(screen, BROWN, home)
    draw_text("HOME", 450, HEIGHT - 45, center=True)

    pygame.draw.rect(screen, YELLOW if stage == "GO_SHOPPING" else (180, 160, 0), market)
    draw_text("MARKET", 125, 300, BLACK, center=True)

    pygame.draw.rect(screen, YELLOW if stage == "MEET_FRIEND" else (180, 160, 0), friend_house)
    draw_text("FRIEND'S HOUSE", 775, 300, BLACK, center=True)

    # ---------- CARS & COLLISIONS ----------
    player_rect = pygame.Rect(player_pos.x, player_pos.y, boy_w, boy_h)
    for car in car_list:
        if not paused:
            car.y += 4
            if car.y > HEIGHT:
                car.y = random.randint(-400, -100)
                car.x = random.choice(lanes)
        draw_car(car)

        # Crash Logic
        in_safe_zone = any(player_rect.colliderect(b) for b in [school, home, market, friend_house])
        if player_rect.colliderect(car) and not in_safe_zone:
            player_pos = pygame.Vector2(440, 520)
            history = []

    # ---------- QUEST LOGIC ----------
    if not paused:
        # 1. MEET FRIEND
        if stage == "MEET_FRIEND" and player_rect.colliderect(friend_house):
            paused = True
            timer = 90  # 1.5 seconds auto-pause
            message = "Waiting for friend..."
            has_friend = True
            stage = "GO_SHOPPING"
            friend_pos = player_pos.copy()

        # 2. GO SHOPPING
        elif stage == "GO_SHOPPING" and player_rect.colliderect(market):
            paused = True
            timer = 120
            message = "Shopping with friend..."
            stage = "GO_SCHOOL"

        # 3. GO SCHOOL
        elif stage == "GO_SCHOOL" and player_rect.colliderect(school):
            paused = True
            timer = 120
            message = "Studying at School..."
            stage = "GO_HOME"

        # 4. BACK HOME
        elif stage == "GO_HOME" and player_rect.colliderect(home):
            paused = True
            message = "Mission Complete! Back Home."
            # Game resets or stops here

    # ---------- RENDER CHARACTERS ----------
    if has_friend:
        draw_character(friend_pos, FRIEND_PURPLE, "Friend")
    draw_character(player_pos, BLUE, "You")

    # ---------- UI & TIMERS ----------
    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        draw_text(message, WIDTH // 2, HEIGHT // 2, color=YELLOW, center=True)

        if timer > 0:
            timer -= 1
        else:
            draw_text("Press any key to continue", WIDTH // 2, HEIGHT // 2 + 50, center=True)

    # Quest Tracker
    pygame.draw.rect(screen, BLACK, (10, 10, 220, 40))
    draw_text(f"Task: {stage.replace('_', ' ')}", 20, 18, YELLOW)

    pygame.display.update()
    clock.tick(60)

pygame.quit()