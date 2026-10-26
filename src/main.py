import pygame
import os
import random

from settings import *
from physics import *
from obstacle import *
from player import Player

pygame.init()
clock = pygame.time.Clock()

# ================= WINDOW =================

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
pygame.display.set_caption("FRIDGO")

# ================= ASSETS =================

asset_path = os.path.join(os.path.dirname(__file__), "..", "assets")

background_path = os.path.join(asset_path, "fridgobg.png")
background_image = pygame.image.load(background_path).convert()

blur_size = (max(1, WIDTH // 2), max(1, HEIGHT // 2))
background_image = pygame.transform.smoothscale(
    background_image, blur_size
)
background_image = pygame.transform.scale(
    background_image, (WIDTH, HEIGHT)
)

ground_path = os.path.join(asset_path, "ground.png")
ground_image = pygame.image.load(ground_path).convert_alpha()
ground_image = pygame.transform.scale(
    ground_image, (WIDTH, GROUND_HEIGHT)
)

platform_path = os.path.join(asset_path, "platform.png")
platform_image = pygame.image.load(platform_path).convert_alpha()


# Collectible sprites

COLLECTIBLE_SIZE = 28

star_path = os.path.join(asset_path, "star.png")

star_image = pygame.image.load(star_path).convert_alpha()

star_image = pygame.transform.scale(

    star_image, (COLLECTIBLE_SIZE, COLLECTIBLE_SIZE)

)

clock_path = os.path.join(asset_path, "clock.png")

clock_image = pygame.image.load(clock_path).convert_alpha()

clock_image = pygame.transform.scale(

    clock_image, (COLLECTIBLE_SIZE, COLLECTIBLE_SIZE)

)

# ================= PLAYER =================

player = Player()

# ================= GAME SETTINGS =================

COLLECTIBLE_SIZE = 28

STAR_COOLDOWN = 3.0
STAR_REPOSITION_INTERVAL = 8.0

CLOCK_MIN_DELAY = 3.0
CLOCK_MAX_DELAY = 8.0
CLOCK_VISIBLE_TIME = 5.0

LEVEL_CHANGE_INTERVAL = 15.0
DIFFICULTY_INTERVAL = 15.0

BASE_MAX_VERTICAL_GAP = 150
BASE_MAX_HORIZONTAL_GAP = 320

score = 0
remaining_time = 30.0

generation_timer = 0.0
star_respawn_timer = 0.0
star_reposition_timer = 0.0

clock_respawn_timer = random.uniform(
    CLOCK_MIN_DELAY, CLOCK_MAX_DELAY
)
clock_visible_timer = 0.0

elapsed_game_time = 0.0

game_font = pygame.font.Font(None, 32)

platforms = []
stars = []
time_clocks = []

# ================= COLLECTIBLE SPAWNING =================

def spawn_collectible(target_platform=None):
    """Spawn a collectible away from the player, on platforms,
    the ground, or in the air."""

    ground_top = HEIGHT - GROUND_HEIGHT
    min_distance = 150

    for _ in range(100):
        # Randomly choose ground, platform, or air
        spawn_type = random.choice(["ground", "platform", "air"])

        if spawn_type == "ground":
            x = random.randint(
                0, WIDTH - COLLECTIBLE_SIZE
            )
            y = ground_top - COLLECTIBLE_SIZE

        elif spawn_type == "platform" and platforms:
            platform = random.choice(platforms)

            x = random.randint(
                platform.left,
                max(platform.left, platform.right - COLLECTIBLE_SIZE)
            )
            y = platform.top - COLLECTIBLE_SIZE

        else:
            x = random.randint(
                0, WIDTH - COLLECTIBLE_SIZE
            )
            y = random.randint(
                80, max(80, ground_top - COLLECTIBLE_SIZE)
            )

        # Keep the star away from the player
        star_rect = pygame.Rect(
            x, y, COLLECTIBLE_SIZE, COLLECTIBLE_SIZE
        )

        player_rect = pygame.Rect(
            round(player.x),
            round(player.y),
            player.width,
            player.height
        )

        if (
            abs(star_rect.centerx - player_rect.centerx) >= min_distance
            or abs(star_rect.centery - player_rect.centery) >= min_distance
        ):
            return star_rect

    # Fallback if a suitable position cannot be found
    return pygame.Rect(
        WIDTH - COLLECTIBLE_SIZE,
        100,
        COLLECTIBLE_SIZE,
        COLLECTIBLE_SIZE
    )


# ================= GENERATE LEVEL =================

def generate_level():
    global platforms, stars, time_clocks

    platforms = []
    stars = []
    time_clocks = []

    number_of_platforms = random.randint(4, 6)

    ground_top = HEIGHT - GROUND_HEIGHT
    attempts = 0

    difficulty_level = int(
        elapsed_game_time // DIFFICULTY_INTERVAL
    )

    max_vertical_gap = max(
        85,
        BASE_MAX_VERTICAL_GAP - difficulty_level * 8
    )

    max_horizontal_gap = max(
        130,
        BASE_MAX_HORIZONTAL_GAP - difficulty_level * 8
    )

    # Starter platform

    starter_width = 160

    starter_x = min(
        max(60, int(player.x) + 40),
        WIDTH - starter_width
    )

    starter_y = ground_top - random.randint(90, 115)

    starter_platform = pygame.Rect(
        starter_x,
        starter_y,
        starter_width,
        30
    )

    platforms.append(starter_platform)

    # Generate remaining platforms

    while len(platforms) < number_of_platforms and attempts < 1000:

        attempts += 1

            # Reduce platform width as time progresses

        size_reduction = min(difficulty_level * 10, 50)

        platform_width = random.randint(

            max(60, 100 - size_reduction),

            max(80, 180 - size_reduction)

        )
        platform_height = 30

        platform_x = random.randint(
            0, WIDTH - platform_width
        )

        platform_y = random.randint(
            140, ground_top - 100
        )

        candidate = pygame.Rect(
            platform_x,
            platform_y,
            platform_width,
            platform_height
        )

        # Avoid excessive overlap

        if any(
            candidate.inflate(20, 20).colliderect(
                existing.inflate(20, 20)
            )
            for existing in platforms
        ):
            continue

        # Keep platforms reasonably reachable

        reachable = any(
            abs(candidate.centerx - existing.centerx)
            <= max_horizontal_gap
            and abs(candidate.top - existing.top)
            <= max_vertical_gap
            for existing in platforms
        )

        if reachable:
            platforms.append(candidate)

    # Spawn one star at the beginning

    if platforms:
        stars.append(
            spawn_collectible(random.choice(platforms))
        )


# ================= START GAME =================

generate_level()
running = True

# ================= MAIN GAME LOOP =================

while running:

    dt = clock.tick(FPS) / 1000.0
    elapsed_game_time += dt

    # ================= INPUT =================

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.direction = -1

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.direction = 1

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.direction = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if (
            event.type == pygame.KEYDOWN
            and player.on_ground
            and event.key == pygame.K_SPACE
        ):
            player.charging = True

        if (
            event.type == pygame.KEYUP
            and event.key == pygame.K_SPACE
        ):
            player.charging = False

            player.velocity_y = -(player.charge * 30)

            player.velocity_x = (
                player.direction * player.charge * 20
            )

            player.on_ground = False
            player.charge = 0

    # ================= CHARGE JUMP =================

    if player.charging:

        player.charge += 25 * dt

        if player.charge > MAX_CHARGE:
            player.charge = MAX_CHARGE

    # ================= SCREEN BOUNDARIES =================

    if player.x < 0:
        player.x = 0

    if player.x + player.width > WIDTH:
        player.x = WIDTH - player.width

    # ================= PHYSICS =================

    update_physics(player, dt, platforms)

    # ================= COUNTDOWN =================

    remaining_time -= dt

    if remaining_time <= 0:
        remaining_time = 0
        running = False
        break

    # ================= PLATFORM REGENERATION =================

    generation_timer += dt

    if generation_timer >= LEVEL_CHANGE_INTERVAL:

        generation_timer = 0.0

        generate_level()
            # Make the frog fall when the old platforms disappear

        player.on_ground = False

        player.velocity_y = max(player.velocity_y, 0)

        star_respawn_timer = 0.0
        star_reposition_timer = 0.0

        time_clocks.clear()

        clock_visible_timer = 0.0

        clock_respawn_timer = random.uniform(
            CLOCK_MIN_DELAY, CLOCK_MAX_DELAY
        )

    # ================= PLAYER RECTANGLE =================

    player_rect = pygame.Rect(
        round(player.x),
        round(player.y),
        player.width,
        player.height
    )

    # ================= STAR RESPAWN / REPOSITION =================

    star_reposition_timer += dt

    if star_respawn_timer > 0:
        star_respawn_timer = max(
            0.0, star_respawn_timer - dt
        )

    # Respawn the star after collection
    if star_respawn_timer == 0 and not stars:
        stars.append(spawn_collectible())
        star_reposition_timer = 0.0

    # Move an uncollected star every 10 seconds

    elif (
        stars
        and star_reposition_timer >= STAR_REPOSITION_INTERVAL
        and platforms
    ):

        stars[:] = [
            spawn_collectible(random.choice(platforms))
        ]

        star_reposition_timer = 0.0

    # ================= CLOCK SPAWN / DISAPPEARANCE =================

    if time_clocks:

        # Countdown while the clock is visible

        clock_visible_timer -= dt

        if clock_visible_timer <= 0:

            # Clock disappeared without being collected

            time_clocks.clear()

            clock_respawn_timer = random.uniform(
                CLOCK_MIN_DELAY, CLOCK_MAX_DELAY
            )

    else:

        # Countdown until the next clock appears

        clock_respawn_timer -= dt

        if clock_respawn_timer <= 0 and platforms:

            # Spawn clock at a random platform

            time_clocks.append(
                spawn_collectible(random.choice(platforms))
            )

            clock_visible_timer = CLOCK_VISIBLE_TIME

    # ================= COLLECT STAR =================

    for star in stars[:]:

        if player_rect.colliderect(star):

            score += 1

            stars.remove(star)

            # Immediately spawn a new star

            if platforms:

               stars.append(spawn_collectible())
            star_respawn_timer = 0.0

            star_reposition_timer = 0.0
    # ================= COLLECT CLOCK =================

    for clock_item in time_clocks[:]:

        if player_rect.colliderect(clock_item):

            remaining_time += 10

            time_clocks.remove(clock_item)

            clock_visible_timer = 0.0

            clock_respawn_timer = random.uniform(
                CLOCK_MIN_DELAY, CLOCK_MAX_DELAY
            )

    # ================= DRAW BACKGROUND =================

    screen.blit(background_image, (0, 0))

    # ================= DRAW GROUND =================

    screen.blit(
        ground_image,
        (0, HEIGHT - GROUND_HEIGHT)
    )

    # ================= DRAW PLATFORMS =================

    for platform in platforms:

        platform_surface = pygame.transform.scale(
            platform_image,
            (platform.width, platform.height)
        )

        screen.blit(
            platform_surface,
            (platform.x, platform.y)
        )

    # ================= DRAW STAR =================

    for star in stars:

        screen.blit(star_image, star.topleft)

    # ================= DRAW CLOCK =================



    for clock_item in time_clocks:

        screen.blit(clock_image, clock_item.topleft)

    # ================= DRAW PLAYER =================

    image = player.get_image()

    draw_x = player.x - (
        image.get_width() - player.width
    ) / 2

    draw_y = player.y + player.sprite_y_offset - (
        image.get_height() - player.height
    ) / 2

    screen.blit(
        image,
        (round(draw_x), round(draw_y))
    )
    # ================= JUMP POWER METER =================

    if player.charging:

        meter_width = 120
        meter_height = 12

        # Meter position above the frog
        meter_x = int(player.x + player.width // 2 - meter_width // 2)
        meter_y = int(player.y - 25)

        # Calculate charge percentage
        charge_percent = min(player.charge / MAX_CHARGE, 1.0)

        # Meter background
        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (meter_x, meter_y, meter_width, meter_height)
        )

        # Filled portion
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (meter_x, meter_y, int(meter_width * charge_percent), meter_height)
        )

        # Border
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (meter_x, meter_y, meter_width, meter_height),
            2
        )
    # ================= SCOREBOARD =================

    score_text = game_font.render(
        f"Stars: {score}", True, (0, 0, 0)
    )

    time_text = game_font.render(
        f"Time: {int(remaining_time)}s", True, (0, 0, 0)
    )

    score_panel = pygame.Rect(
        12,
        12,
        score_text.get_width() + 24,
        score_text.get_height() + 14
    )

    time_panel = pygame.Rect(
        12,
        score_panel.bottom + 8,
        time_text.get_width() + 24,
        time_text.get_height() + 14
    )

    pygame.draw.rect(
        screen, (255, 255, 255), score_panel
    )

    pygame.draw.rect(
        screen, (255, 255, 255), time_panel
    )

    pygame.draw.rect(
        screen, (0, 0, 0), score_panel, 2
    )

    pygame.draw.rect(
        screen, (0, 0, 0), time_panel, 2
    )

    screen.blit(
        score_text,
        (score_panel.x + 12, score_panel.y + 7)
    )

    screen.blit(
        time_text,
        (time_panel.x + 12, time_panel.y + 7)
    )

    pygame.display.flip()


# ================= GAME OVER SCREEN =================

if remaining_time <= 0:

    overlay = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 180))

    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 76)
    result_font = pygame.font.Font(None, 42)

    game_over_text = title_font.render(
        "GAME OVER", True, (255, 255, 255)
    )

    final_score_text = result_font.render(
        f"Final Stars: {score}", True, (255, 215, 0)
    )

    instruction_text = game_font.render(
        "Close the window to exit",
        True,
        (255, 255, 255)
    )

    screen.blit(
        game_over_text,
        game_over_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 60)
        )
    )

    screen.blit(
        final_score_text,
        final_score_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 5)
        )
    )

    screen.blit(
        instruction_text,
        instruction_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 55)
        )
    )

    pygame.display.flip()

    # Keep Game Over screen visible until window closes

    waiting_for_exit = True

    while waiting_for_exit:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                waiting_for_exit = False

        clock.tick(30)


pygame.quit()