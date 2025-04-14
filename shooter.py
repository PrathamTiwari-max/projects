import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Screen Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wild West Showdown")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 223, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SAND = (194, 178, 128)
SKY_BLUE = (135, 206, 235)

# Font
title_font = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Load images (or create placeholders if images aren't available)
def load_image(name, size, color):
    try:
        image = pygame.image.load(os.path.join('assets', name))
        return pygame.transform.scale(image, size)
    except:
        # Create a placeholder if image file not found
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (0, 0, size[0], size[1]))
        return surface

# Load sounds (or create empty sounds if files aren't available)
def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join('assets', name))
    except:
        # Return a dummy sound object if file not found
        dummy = pygame.mixer.Sound(pygame.mixer.Sound.get_length)  # Just to get a valid Sound object
        dummy.play = lambda: None  # Replace play method with no-op function
        return dummy

# Game assets
try:
    os.makedirs('assets', exist_ok=True)
except:
    pass

# Create a dummy sound for when sound files are missing
class DummySound:
    def play(self):
        pass

# Sound effects
try:
    shoot_sound = pygame.mixer.Sound(os.path.join('assets', 'shoot.wav'))
except:
    shoot_sound = DummySound()
    
try:
    hit_sound = pygame.mixer.Sound(os.path.join('assets', 'hit.wav'))
except:
    hit_sound = DummySound()
    
try:
    death_sound = pygame.mixer.Sound(os.path.join('assets', 'death.wav'))
except:
    death_sound = DummySound()

# Background elements
def draw_background():
    # Sky
    screen.fill(SKY_BLUE)
    
    # Ground
    pygame.draw.rect(screen, SAND, (0, HEIGHT - 150, WIDTH, 150))
    
    # Mountains in background
    pygame.draw.polygon(screen, (100, 100, 100), [(0, HEIGHT - 150), (200, HEIGHT - 250), (400, HEIGHT - 150)])
    pygame.draw.polygon(screen, (80, 80, 80), [(300, HEIGHT - 150), (500, HEIGHT - 300), (700, HEIGHT - 150)])
    
    # Sun
    pygame.draw.circle(screen, YELLOW, (700, 100), 50)
    
    # Cacti
    pygame.draw.rect(screen, GREEN, (150, HEIGHT - 200, 20, 50))
    pygame.draw.rect(screen, GREEN, (155, HEIGHT - 230, 10, 30))
    
    pygame.draw.rect(screen, GREEN, (650, HEIGHT - 180, 20, 30))
    pygame.draw.rect(screen, GREEN, (640, HEIGHT - 170, 15, 20))
    pygame.draw.rect(screen, GREEN, (665, HEIGHT - 170, 15, 20))

# Draw health bar with heart icons
def draw_health_bar(x, y, health, max_health=3):
    for i in range(max_health):
        if i < health:
            # Full heart
            pygame.draw.polygon(screen, RED, [
                (x + i*40 + 20, y + 5),
                (x + i*40 + 10, y + 15),
                (x + i*40 + 20, y + 25),
                (x + i*40 + 30, y + 15),
            ])
            pygame.draw.circle(screen, RED, (x + i*40 + 15, y + 15), 7)
            pygame.draw.circle(screen, RED, (x + i*40 + 25, y + 15), 7)
        else:
            # Empty heart
            pygame.draw.polygon(screen, (100, 100, 100), [
                (x + i*40 + 20, y + 5),
                (x + i*40 + 10, y + 15),
                (x + i*40 + 20, y + 25),
                (x + i*40 + 30, y + 15),
            ], 2)
            pygame.draw.circle(screen, (100, 100, 100), (x + i*40 + 15, y + 15), 7, 2)
            pygame.draw.circle(screen, (100, 100, 100), (x + i*40 + 25, y + 15), 7, 2)

# Particle system for visual effects
class Particle:
    def __init__(self, x, y, color, velocity_range=(-2, 2), size_range=(2, 5), life=20):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(size_range[0], size_range[1])
        self.vel_x = random.uniform(velocity_range[0], velocity_range[1])
        self.vel_y = random.uniform(velocity_range[0], velocity_range[1])
        self.life = life
        self.alpha = 255
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1
        self.alpha = int((self.life / 20) * 255)
        return self.life > 0
        
    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (self.size, self.size), self.size)
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

particles = []

# Home Screen
def home_screen():
    title_y = HEIGHT // 4
    title_direction = 1
    selected_option = 0
    options = ["Single Player", "Multiplayer", "How to Play", "Quit"]
    
    while True:
        # Animate title
        title_y += 0.5 * title_direction
        if title_y > HEIGHT // 4 + 10 or title_y < HEIGHT // 4 - 10:
            title_direction *= -1
        
        # Draw background
        draw_background()
        
        # Draw title
        title = title_font.render("Wild West Showdown", True, WHITE)
        title_shadow = title_font.render("Wild West Showdown", True, BLACK)
        screen.blit(title_shadow, (WIDTH // 2 - title.get_width() // 2 + 3, title_y + 3))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, title_y))
        
        # Draw menu options
        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            option_text = font.render(option, True, color)
            y_pos = HEIGHT // 2 + (i * 50)
            
            # Draw selection indicator
            if i == selected_option:
                pygame.draw.polygon(screen, YELLOW, [
                    (WIDTH // 2 - option_text.get_width() // 2 - 30, y_pos + 10),
                    (WIDTH // 2 - option_text.get_width() // 2 - 15, y_pos + 18),
                    (WIDTH // 2 - option_text.get_width() // 2 - 30, y_pos + 26)
                ])
                pygame.draw.polygon(screen, YELLOW, [
                    (WIDTH // 2 + option_text.get_width() // 2 + 30, y_pos + 10),
                    (WIDTH // 2 + option_text.get_width() // 2 + 15, y_pos + 18),
                    (WIDTH // 2 + option_text.get_width() // 2 + 30, y_pos + 26)
                ])
                
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, y_pos))
        
        # Bottom text
        version_text = small_font.render("v2.0", True, WHITE)
        screen.blit(version_text, (10, HEIGHT - 30))
        
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Single Player
                        return 1
                    elif selected_option == 1:  # Multiplayer
                        return 2
                    elif selected_option == 2:  # How to Play
                        show_instructions()
                    elif selected_option == 3:  # Quit
                        pygame.quit()
                        exit()

def show_instructions():
    running = True
    while running:
        screen.fill(BROWN)
        
        # Title
        title = font.render("How to Play", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        # Instructions
        instructions = [
            "Player 1 (Blue):",
            "- Move: LEFT and RIGHT arrow keys",
            "- Shoot: SPACE",
            "",
            "Player 2 / AI (Red):",
            "- Move: A and D keys (Multiplayer)",
            "- Shoot: ENTER/RETURN (Multiplayer)",
            "",
            "Collect powerups that appear during gameplay!",
            "",
            "Press ESC to return to menu"
        ]
        
        for i, line in enumerate(instructions):
            instruction_text = small_font.render(line, True, WHITE)
            screen.blit(instruction_text, (WIDTH // 2 - 150, 120 + i * 30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

# Player Class
class Cowboy(pygame.sprite.Sprite):
    def __init__(self, x, y, color, is_ai=False, player_num=1):
        super().__init__()
        self.player_num = player_num
        self.original_image = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        # Draw cowboy shape
        # Hat
        pygame.draw.rect(self.original_image, BLACK, (5, 0, 30, 10))
        pygame.draw.rect(self.original_image, BLACK, (0, 10, 40, 5))
        
        # Head
        pygame.draw.circle(self.original_image, (222, 184, 135), (20, 25), 10)
        
        # Body
        pygame.draw.rect(self.original_image, color, (10, 35, 20, 25))
        
        # Arms
        pygame.draw.rect(self.original_image, color, (0, 35, 10, 5))
        pygame.draw.rect(self.original_image, color, (30, 35, 10, 5))
        
        # Gun
        self.gun_side = 30 if player_num == 1 else 0
        pygame.draw.rect(self.original_image, BLACK, (self.gun_side, 40, 10 if player_num == 1 else -10, 5))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.is_ai = is_ai
        self.shoot_cooldown = 0
        self.health = 3
        self.score = 0
        self.max_health = 3
        
        # Power-ups
        self.power_up_timer = 0
        self.has_power_up = None
        
        # Animation
        self.hit_animation = 0
        
        # Movement for dodging
        self.target_x = x
        
    def update(self, left, right):
        # Update hit animation
        if self.hit_animation > 0:
            self.hit_animation -= 1
            # Flash red when hit
            if self.hit_animation % 6 < 3:
                self.image = self.original_image.copy()
                self.image.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
            else:
                self.image = self.original_image.copy()
        else:
            self.image = self.original_image.copy()
            
        # Display power-up indicator
        if self.has_power_up:
            color = YELLOW if self.has_power_up == "rapid_fire" else GREEN if self.has_power_up == "shield" else BLUE
            pygame.draw.circle(self.image, color, (35, 10), 5)
            
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.has_power_up = None
        
        # Movement
        if not self.is_ai:
            keys = pygame.key.get_pressed()
            if keys[left] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[right] and self.rect.right < WIDTH:
                self.rect.x += self.speed
        else:
            # Improved AI Movement
            if self.shoot_cooldown <= 0:
                # Stop to aim and shoot
                self.target_x = player1.rect.x
                if random.random() < 0.5:
                    # Add some randomness to make it imperfect
                    self.target_x += random.randint(-100, 100)
                    self.target_x = max(50, min(WIDTH - 50, self.target_x))
            else:
                # Move randomly when not shooting
                if random.random() < 0.03:
                    self.target_x = random.randint(50, WIDTH - 50)
            
            # Dodge bullets
            for bullet in bullets:
                if bullet.shooter != self and abs(self.rect.centerx - bullet.rect.centerx) < 50 and abs(bullet.rect.centery - self.rect.centery) < 150:
                    # Dodge to the side
                    if self.rect.centerx < bullet.rect.centerx:
                        self.target_x = max(50, self.rect.centerx - 100)
                    else:
                        self.target_x = min(WIDTH - 50, self.rect.centerx + 100)
                    break
            
            # Move toward target position
            if abs(self.rect.centerx - self.target_x) > self.speed:
                if self.rect.centerx < self.target_x:
                    self.rect.x += self.speed
                else:
                    self.rect.x -= self.speed
            
            # AI Shooting Logic
            if self.shoot_cooldown <= 0:
                # Smarter shooting - aim at player with some randomness
                chance_to_shoot = 0.1
                if abs(self.rect.centerx - player1.rect.centerx) < 100:
                    chance_to_shoot = 0.3  # More likely to shoot when aligned
                
                if random.random() < chance_to_shoot:
                    self.shoot(bullets, 1)
                    self.shoot_cooldown = random.randint(30, 60)
                    
                    # If has rapid fire, shoot multiple bullets
                    if self.has_power_up == "rapid_fire":
                        pygame.time.set_timer(pygame.USEREVENT + 3, 200)  # Schedule additional shots
            else:
                self.shoot_cooldown -= 1
    
    def shoot(self, bullet_group, direction):
        # Play sound
        shoot_sound.play()
        
        # Create bullet
        x_offset = 20 if self.player_num == 1 else -20
        bullet = Bullet(self.rect.centerx + x_offset, 
                       self.rect.top if direction == -1 else self.rect.bottom, 
                       direction, self)
        bullet_group.add(bullet)
        self.bullets.add(bullet)
        
        # Create muzzle flash particles
        for _ in range(10):
            particles.append(Particle(
                self.rect.centerx + x_offset, 
                self.rect.top if direction == -1 else self.rect.bottom,
                (255, 255, 0),
                (-3, 3) if direction == -1 else (-3, 3),
                (2, 4),
                15
            ))
    
    def take_damage(self):
        # If has shield, don't take damage
        if self.has_power_up == "shield":
            return False
            
        hit_sound.play()
        self.health -= 1
        self.hit_animation = 30  # Set hit animation frames
        
        # Create blood particles
        for _ in range(20):
            particles.append(Particle(
                self.rect.centerx, self.rect.centery,
                (255, 0, 0),
                (-3, 3),
                (1, 3),
                30
            ))
        
        if self.health <= 0:
            death_sound.play()
            return True  # Player is defeated
        return False

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, shooter):
        super().__init__()
        self.image = pygame.Surface((8, 15), pygame.SRCALPHA)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10 * direction
        self.shooter = shooter
        
        # Trail particles
        self.trail_timer = 0
    
    def update(self):
        self.rect.y += self.speed
        
        # Create trail particles
        self.trail_timer += 1
        if self.trail_timer >= 3:
            self.trail_timer = 0
            particles.append(Particle(
                self.rect.centerx, self.rect.centery,
                (255, 255, 0),
                (-0.5, 0.5),
                (1, 3),
                10
            ))
        
        # Remove if out of screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
        
        # Check for collisions handled in main game loop

# PowerUp Class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.type = random.choice(["health", "rapid_fire", "shield"])
        
        if self.type == "health":
            color = RED
        elif self.type == "rapid_fire":
            color = YELLOW
        else:  # shield
            color = BLUE
            
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (12, 12), 12)
        
        # Draw a symbol based on the power-up type
        if self.type == "health":
            pygame.draw.rect(self.image, WHITE, (5, 10, 15, 5))
            pygame.draw.rect(self.image, WHITE, (10, 5, 5, 15))
        elif self.type == "rapid_fire":
            pygame.draw.polygon(self.image, WHITE, [(5, 12), (15, 5), (15, 20)])
            pygame.draw.polygon(self.image, WHITE, [(12, 12), (22, 5), (22, 20)])
        else:  # shield
            pygame.draw.circle(self.image, WHITE, (12, 12), 8, 2)
            pygame.draw.line(self.image, WHITE, (12, 4), (12, 12), 2)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 2
        self.vel_x = random.uniform(-1, 1)
        
    def update(self):
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        
        # Bounce off walls
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel_x *= -1
        
        # Remove if out of screen
        if self.rect.top > HEIGHT:
            self.kill()

def game_over_screen(winner):
    running = True
    alpha = 0
    fade_in = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if alpha >= 255:  # Only allow key presses when fully faded in
                    running = False
        
        # Fade effect
        if fade_in:
            alpha += 5
            if alpha >= 255:
                alpha = 255
                fade_in = False
        
        # Draw background with transparency
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        if alpha > 50:  # Only start displaying text after some fade
            game_over = title_font.render("GAME OVER", True, WHITE)
            screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 3))
            
            winner_text = font.render(f"{winner} wins!", True, YELLOW)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            
            if alpha >= 255:
                continue_text = small_font.render("Press any key to continue", True, WHITE)
                screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT * 2 // 3))
        
        pygame.display.flip()
        pygame.time.delay(30)

def pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    pause_text = title_font.render("PAUSED", True, WHITE)
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))
    
    resume_text = font.render("Press P to Resume", True, WHITE)
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
    
    quit_text = font.render("Press Q to Quit", True, WHITE)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.flip()
    
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:
                    return True  # Quit game
    
    return False  # Continue game

# Main game loop
def main_game(mode):
    global bullets, particles, player1
    
    # Setup Players
    player1 = Cowboy(WIDTH // 2, HEIGHT - 100, BLUE, player_num=1)
    if mode == 1:
        player2 = Cowboy(WIDTH // 2, 100, RED, is_ai=True, player_num=2)  # AI-controlled enemy
    else:
        player2 = Cowboy(WIDTH // 2, 100, RED, player_num=2)  # Second player

    player_group = pygame.sprite.Group(player1, player2)
    bullets = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    
    particles = []  # Reset particles
    
    # Game timers
    power_up_timer = 0
    game_time = 0
    
    # AI additional shot event for rapid fire
    AI_RAPID_FIRE = pygame.USEREVENT + 3
    AI_rapid_fire_count = 0
    
    # Game Loop
    running = True
    while running:
        game_time += 1
        
        # Draw background
        draw_background()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.shoot(bullets, -1)
                    # If has rapid fire, shoot multiple bullets
                    if player1.has_power_up == "rapid_fire":
                        pygame.time.set_timer(pygame.USEREVENT + 1, 200)  # Schedule additional shots
                        pygame.time.set_timer(pygame.USEREVENT + 2, 400)  # Schedule additional shots
                if mode == 2 and event.key == pygame.K_RETURN:
                    player2.shoot(bullets, 1)
                    # If has rapid fire, shoot multiple bullets
                    if player2.has_power_up == "rapid_fire":
                        pygame.time.set_timer(pygame.USEREVENT + 4, 200)  # Schedule additional shots
                        pygame.time.set_timer(pygame.USEREVENT + 5, 400)  # Schedule additional shots
                if event.key == pygame.K_p:
                    if pause_menu():
                        return  # Quit to main menu
            
            # Handle rapid fire powerup for Player 1
            if event.type == pygame.USEREVENT + 1 or event.type == pygame.USEREVENT + 2:
                player1.shoot(bullets, -1)
                
            # Handle rapid fire powerup for AI
            if event.type == AI_RAPID_FIRE and AI_rapid_fire_count < 2:
                player2.shoot(bullets, 1)
                AI_rapid_fire_count += 1
                if AI_rapid_fire_count >= 2:
                    AI_rapid_fire_count = 0
                    pygame.time.set_timer(AI_RAPID_FIRE, 0)  # Cancel timer
                    
            # Handle rapid fire powerup for Player 2
            if event.type == pygame.USEREVENT + 4 or event.type == pygame.USEREVENT + 5:
                player2.shoot(bullets, 1)
        
        # Update game objects
        player1.update(pygame.K_LEFT, pygame.K_RIGHT)
        if mode == 1:
            player2.update(None, None)
        else:
            player2.update(pygame.K_a, pygame.K_d)
        bullets.update()
        power_ups.update()
        
        # Update particles
        particles = [p for p in particles if p.update()]
        
        # Check for bullet collisions
        for bullet in bullets:
            if bullet.shooter == player1 and bullet.rect.colliderect(player2.rect):
                if player2.take_damage():
                    player1.score += 1
                    game_over_screen("Player 1")
                    return
                bullet.kill()
            elif bullet.shooter == player2 and bullet.rect.colliderect(player1.rect):
                if player1.take_damage():
                    player2.score += 1
                    winner = "AI" if mode == 1 else "Player 2"
                    game_over_screen(winner)
                    return
                bullet.kill()
        
        # Check for power-up collisions
        for power_up in power_ups:
            if power_up.rect.colliderect(player1.rect):
                if power_up.type == "health":
                    player1.health = min(player1.max_health, player1.health + 1)
                else:
                    player1.has_power_up = power_up.type
                    player1.power_up_timer = 300  # 10 seconds
                power_up.kill()
            elif power_up.rect.colliderect(player2.rect):
                if power_up.type == "health":
                    player2.health = min(player2.max_health, player2.health + 1)
                else:
                    player2.has_power_up = power_up.type
                    player2.power_up_timer = 300  # 10 seconds
                power_up.kill()
        
        # Spawn power-ups randomly
        power_up_timer += 1
        if power_up_timer > 300 and random.random() < 0.01:  # Average one powerup every 10 seconds
            power_ups.add(PowerUp(random.randint(50, WIDTH - 50), 0))
            power_up_timer = 0
        
        # Draw game objects
        player_group.draw(screen)
        bullets.draw(screen)
        power_ups.draw(screen)
        
        # Draw particles
        for particle in particles:
            particle.draw(screen)
        
        # Draw HUD
        draw_health_bar(50, HEIGHT - 50, player1.health)
        draw_health_bar(50, 30, player2.health)
        
        # Draw scores
        score_text = font.render(f"Score: {player1.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, HEIGHT - 50))
        
        # Update display
        pygame.display.flip()
        pygame.time.delay(30)
        # Main program execution
if __name__ == "__main__":
    # Game loop
    running = True
    while running:
        # Start at home screen
        mode = home_screen()
        
        # Run main game with selected mode
        if mode in [1, 2]:  # 1 = Single Player, 2 = Multiplayer
            main_game(mode)
        
        # Check for program exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    # Clean up and exit
    pygame.quit()