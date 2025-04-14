import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)  # Sky blue
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
current_state = MENU

# Game variables
clock = pygame.time.Clock()
FPS = 60
gravity = 0.5
flap_strength = -8
score = 0

# Bird properties
class Bird:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, 30, 30)
        self.velocity = 0
        self.angle = 0
        self.animation_frames = []
        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0
        
        # Create simple bird animation frames (yellow circle with wing positions)
        for i in range(4):
            surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(surface, YELLOW, (15, 15), 15)
            # Draw wing at different positions
            wing_offset = math.sin(i * math.pi / 2) * 5
            pygame.draw.ellipse(surface, ORANGE, (5, 15 + wing_offset, 15, 5))
            self.animation_frames.append(surface)

    def update(self):
        self.velocity += gravity
        self.rect.y += self.velocity
        
        # Update rotation based on velocity
        self.angle = max(-30, min(self.velocity * 2, 90))
        
        # Update animation
        self.animation_time += 1
        if self.animation_time >= FPS * self.animation_speed:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def draw(self, surface):
        # Rotate the current frame
        rotated_frame = pygame.transform.rotate(self.animation_frames[self.current_frame], -self.angle)
        new_rect = rotated_frame.get_rect(center=self.rect.center)
        surface.blit(rotated_frame, new_rect.topleft)

    def flap(self):
        self.velocity = flap_strength

class Pipe:
    def __init__(self, x):
        self.gap_size = 150
        self.gap_y = random.randint(150, HEIGHT - 150 - self.gap_size)
        self.x = x
        self.width = 50
        self.speed = 3
        self.passed = False
        
        # Create gradient-colored pipes
        self.top_pipe = self.create_pipe_surface(self.gap_y)
        self.bottom_pipe = self.create_pipe_surface(HEIGHT - (self.gap_y + self.gap_size))
        
    def create_pipe_surface(self, height):
        surface = pygame.Surface((self.width, height), pygame.SRCALPHA)
        for i in range(height):
            # Create a gradient from dark to light green
            color = (0, 200 + (i % 55), 0)
            pygame.draw.line(surface, color, (0, i), (self.width, i))
        # Add highlight and shadow
        pygame.draw.rect(surface, (255, 255, 255, 64), (0, 0, 5, height))
        pygame.draw.rect(surface, (0, 0, 0, 64), (self.width-5, 0, 5, height))
        return surface

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        surface.blit(self.top_pipe, (self.x, 0))
        surface.blit(self.bottom_pipe, (self.x, self.gap_y + self.gap_size))

    def collides_with(self, bird_rect):
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + self.gap_size, 
                                     self.width, HEIGHT - (self.gap_y + self.gap_size))
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 30, 255), 
                          min(color[1] + 30, 255), 
                          min(color[2] + 30, 255))
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered() else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

class Game:
    def __init__(self):
        self.reset_game()
        self.high_score = 0
        
        # Create buttons
        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        self.start_button = Button(button_x, HEIGHT // 2 - button_height,
                                 button_width, button_height, "Start Game", (100, 200, 100))
        self.quit_button = Button(button_x, HEIGHT // 2 + button_height,
                                button_width, button_height, "Quit", (200, 100, 100))
        
        # Create clouds for background
        self.clouds = []
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT//2),
                'speed': random.uniform(0.5, 1.5),
                'size': random.randint(30, 60)
            })

    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.spawn_pipe()

    def spawn_pipe(self):
        self.pipes.append(Pipe(WIDTH))

    def update_clouds(self):
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -cloud['size']:
                cloud['x'] = WIDTH + cloud['size']
                cloud['y'] = random.randint(0, HEIGHT//2)

    def draw_clouds(self, surface):
        for cloud in self.clouds:
            pygame.draw.circle(surface, WHITE, 
                             (int(cloud['x']), int(cloud['y'])), 
                             cloud['size'])
            pygame.draw.circle(surface, WHITE, 
                             (int(cloud['x'] - cloud['size']//2), int(cloud['y'])), 
                             cloud['size']//1.5)
            pygame.draw.circle(surface, WHITE, 
                             (int(cloud['x'] + cloud['size']//2), int(cloud['y'])), 
                             cloud['size']//1.5)

    def draw_background(self):
        # Draw sky gradient
        for i in range(HEIGHT):
            color = (135, 206, 235 - i//10)  # Gradually darker blue
            pygame.draw.line(screen, color, (0, i), (WIDTH, i))
        
        # Draw clouds
        self.draw_clouds(screen)

    def run(self):
        global current_state
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_state == MENU:
                        if self.start_button.is_hovered():
                            current_state = PLAYING
                            self.reset_game()
                        elif self.quit_button.is_hovered():
                            pygame.quit()
                            sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if current_state == PLAYING:
                            self.bird.flap()
                        elif current_state == GAME_OVER:
                            current_state = MENU
            
            # Update clouds in all states
            self.update_clouds()
            
            # Draw background
            self.draw_background()
            
            if current_state == MENU:
                self.draw_menu()
            elif current_state == PLAYING:
                self.update_game()
                self.draw_game()
            elif current_state == GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            clock.tick(FPS)

    def update_game(self):
        global current_state
        
        self.bird.update()
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
            # Check for score
            if not pipe.passed and pipe.x + pipe.width < self.bird.rect.x:
                pipe.passed = True
                self.score += 1
            
            # Check for collision
            if pipe.collides_with(self.bird.rect):
                self.high_score = max(self.score, self.high_score)
                current_state = GAME_OVER
        
        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if pipe.x > -pipe.width]
        
        # Spawn new pipes
        if len(self.pipes) == 0 or self.pipes[-1].x < WIDTH - 200:
            self.spawn_pipe()
        
        # Check for out of bounds
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= HEIGHT:
            self.high_score = max(self.score, self.high_score)
            current_state = GAME_OVER

    def draw_menu(self):
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Flappy Bird", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title_text, title_rect)
        
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
        
        if self.high_score > 0:
            high_score_font = pygame.font.Font(None, 36)
            high_score_text = high_score_font.render(f"High Score: {self.high_score}", True, BLACK)
            high_score_rect = high_score_text.get_rect(center=(WIDTH//2, HEIGHT*3//4))
            screen.blit(high_score_text, high_score_rect)

    def draw_game(self):
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(screen)
        
        # Draw bird
        self.bird.draw(screen)
        
        # Draw score
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(str(self.score), True, BLACK)
        score_rect = score_text.get_rect(center=(WIDTH//2, 50))
        screen.blit(score_text, score_rect)

    def draw_game_over(self):
        # Draw the game state first
        self.draw_game()
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw Game Over text
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over!", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(game_over_text, text_rect)
        
        # Draw score
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(score_text, score_rect)
        
        # Draw high score
        high_score_text = score_font.render(f"High Score: {self.high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(high_score_text, high_score_rect)
        
        # Draw instruction
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Press SPACE to return to menu", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT*3//4))
        screen.blit(instruction_text, instruction_rect)

# Start the game
game = Game()
game.run()