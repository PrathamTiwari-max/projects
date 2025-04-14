import pygame
import random
import sys

# Initialize pygame
pygame.init()
pygame.font.init()

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Color Palette
COLORS = {
    'BACKGROUND': (20, 20, 40),
    'GRID_BG': (30, 30, 60),
    'TEXT': (230, 230, 250),
    'ACCENT': (100, 149, 237),
    'SHADOW': (10, 10, 20),
    'PIECES': {
        'I': (0, 255, 255),    # Cyan
        'O': (255, 255, 0),    # Yellow
        'T': (128, 0, 128),    # Purple
        'J': (0, 0, 255),      # Blue
        'L': (255, 165, 0),    # Orange
        'S': (0, 255, 0),      # Green
        'Z': (255, 0, 0)       # Red
    }
}

# Tetromino shapes
SHAPES = {
    'T': [[1, 1, 1], [0, 1, 0]],
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'L': [[1, 0, 0], [1, 1, 1]],
    'J': [[0, 0, 1], [1, 1, 1]]
}

class Tetris:
    def __init__(self):
        # Screen setup with better resolution and scaling
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Premium Tetris')
        
        # Enhanced icon
        icon = pygame.Surface((32, 32))
        icon.fill(COLORS['ACCENT'])
        pygame.draw.rect(icon, COLORS['PIECES']['T'], (10, 10, 12, 12))
        pygame.display.set_icon(icon)
        
        # Clock and fonts
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 60)
        self.main_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Background gradient setup
        self.create_background()

        # Game state
        self.reset_game()

    def reset_game(self):
        # Initialize game grid
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        
        # Game statistics
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        
        # Piece management
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        
        # Piece position
        self.piece_pos = [GRID_WIDTH // 2 - len(self.current_piece['shape'][0]) // 2, 0]
        
        # Timing and speed
        self.fall_time = 0
        self.fall_speed = 0.5  # Initial fall speed

    def get_new_piece(self):
        # Select a random shape
        shape_name = random.choice(list(SHAPES.keys()))
        return {
            'shape': SHAPES[shape_name],
            'color': COLORS['PIECES'][shape_name],
            'name': shape_name
        }

    def create_background(self):
        # Create a gradient background
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            # Create a smooth gradient from dark blue to even darker blue
            r = int(20 + y * (10 / SCREEN_HEIGHT))
            g = int(20 + y * (10 / SCREEN_HEIGHT))
            b = int(40 + y * (20 / SCREEN_HEIGHT))
            pygame.draw.line(self.background, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_shadowed_text(self, text, font, color, position, shadow_offset=2):
        # Draw text with a shadow effect
        shadow_text = font.render(text, True, COLORS['SHADOW'])
        main_text = font.render(text, True, color)
        
        shadow_rect = shadow_text.get_rect(topleft=(position[0] + shadow_offset, position[1] + shadow_offset))
        main_rect = main_text.get_rect(topleft=position)
        
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(main_text, main_rect)

    def draw_grid(self):
        # Draw a more stylish grid
        grid_rect = pygame.Rect(0, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(self.screen, COLORS['GRID_BG'], grid_rect)
        
        # Subtle grid lines
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, COLORS['ACCENT'], 
                             (x * BLOCK_SIZE, 0), 
                             (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 1)
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, COLORS['ACCENT'], 
                             (0, y * BLOCK_SIZE), 
                             (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE), 1)

        # Existing blocks with glow effect
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    block_rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    # Main block
                    pygame.draw.rect(self.screen, cell, block_rect)
                    # Subtle glow
                    glow_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                    glow_surface.fill((*cell, 100))
                    self.screen.blit(glow_surface, block_rect)

    def draw_current_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_piece['color'],
                                     ((self.piece_pos[0] + x) * BLOCK_SIZE, 
                                      (self.piece_pos[1] + y) * BLOCK_SIZE, 
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_ui(self):
        # Title
        self.draw_shadowed_text('TETRIS', self.title_font, COLORS['ACCENT'], (GRID_WIDTH * BLOCK_SIZE + 50, 50))
        
        # Score section with improved styling
        score_x = GRID_WIDTH * BLOCK_SIZE + 50
        score_y = 200
        
        self.draw_shadowed_text(f'Score: {self.score}', self.main_font, COLORS['TEXT'], (score_x, score_y))
        self.draw_shadowed_text(f'Level: {self.level}', self.main_font, COLORS['TEXT'], (score_x, score_y + 50))
        self.draw_shadowed_text(f'Lines: {self.lines_cleared}', self.main_font, COLORS['TEXT'], (score_x, score_y + 100))

        # Next piece preview with a styled frame
        preview_x = GRID_WIDTH * BLOCK_SIZE + 50
        preview_y = 400
        preview_rect = pygame.Rect(preview_x - 10, preview_y - 40, 120, 120)
        pygame.draw.rect(self.screen, COLORS['GRID_BG'], preview_rect)
        pygame.draw.rect(self.screen, COLORS['ACCENT'], preview_rect, 2)
        
        self.draw_shadowed_text('Next Piece', self.small_font, COLORS['TEXT'], (preview_x, preview_y - 40))
        
        # Draw next piece in preview
        for y, row in enumerate(self.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece['color'],
                                     (preview_x + x * BLOCK_SIZE, 
                                      preview_y + y * BLOCK_SIZE, 
                                      BLOCK_SIZE, BLOCK_SIZE))

    def is_valid_move(self, piece, offset):
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = offset[0] + x
                    grid_y = offset[1] + y
                    
                    # Check boundaries
                    if (grid_x < 0 or grid_x >= GRID_WIDTH or 
                        grid_y >= GRID_HEIGHT):
                        return False
                    
                    # Check collisions with existing blocks
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.piece_pos[0] + x
                    grid_y = self.piece_pos[1] + y
                    if 0 <= grid_y < GRID_HEIGHT:
                        self.grid[grid_y][grid_x] = self.current_piece['color']

    def clear_lines(self):
        # Remove complete lines and update score
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0] * GRID_WIDTH)
        
        # Update score and level
        lines_count = len(lines_to_clear)
        if lines_count > 0:
            self.lines_cleared += lines_count
            # Scoring system
            score_multiplier = {1: 40, 2: 100, 3: 300, 4: 1200}
            self.score += score_multiplier.get(lines_count, 0) * self.level
            
            # Level up every 10 lines
            self.level = self.lines_cleared // 10 + 1
            # Increase speed as level increases
            self.fall_speed = max(0.05, 0.5 - (self.level * 0.05))

    def rotate_piece(self):
        # Rotate the current piece
        rotated = list(zip(*self.current_piece['shape'][::-1]))
        if self.is_valid_move(rotated, self.piece_pos):
            self.current_piece['shape'] = rotated

    def run(self):
        # Main game loop
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            new_pos = [self.piece_pos[0] - 1, self.piece_pos[1]]
                            if self.is_valid_move(self.current_piece['shape'], new_pos):
                                self.piece_pos = new_pos
                        
                        elif event.key == pygame.K_RIGHT:
                            new_pos = [self.piece_pos[0] + 1, self.piece_pos[1]]
                            if self.is_valid_move(self.current_piece['shape'], new_pos):
                                self.piece_pos = new_pos
                        
                        elif event.key == pygame.K_DOWN:
                            new_pos = [self.piece_pos[0], self.piece_pos[1] + 1]
                            if self.is_valid_move(self.current_piece['shape'], new_pos):
                                self.piece_pos = new_pos
                        
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        
                        elif event.key == pygame.K_SPACE:
                            # Hard drop
                            while self.is_valid_move(self.current_piece['shape'], 
                                                     [self.piece_pos[0], self.piece_pos[1] + 1]):
                                self.piece_pos[1] += 1
                
                if event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()

            # Game logic
            if not self.game_over:
                current_time = pygame.time.get_ticks()
                
                # Automatic piece drop
                if current_time - self.fall_time > self.fall_speed * 1000:
                    new_pos = [self.piece_pos[0], self.piece_pos[1] + 1]
                    
                    if self.is_valid_move(self.current_piece['shape'], new_pos):
                        self.piece_pos = new_pos
                    else:
                        # Lock the piece
                        self.lock_piece()
                        self.clear_lines()
                        
                        # New piece
                        self.current_piece = self.next_piece
                        self.next_piece = self.get_new_piece()
                        self.piece_pos = [GRID_WIDTH // 2 - len(self.current_piece['shape'][0]) // 2, 0]
                        
                        # Check game over
                        if not self.is_valid_move(self.current_piece['shape'], self.piece_pos):
                            self.game_over = True
                    
                    self.fall_time = current_time

            # Drawing
            self.screen.blit(self.background, (0, 0))
            self.draw_grid()
            
            if not self.game_over:
                self.draw_current_piece()
            
            self.draw_ui()
            
            # Game over screen
            if self.game_over:
                game_over_text = self.title_font.render('GAME OVER', True, COLORS['PIECES']['Z'])
                restart_text = self.main_font.render('Press R to Restart', True, COLORS['TEXT'])
                self.screen.blit(game_over_text, (GRID_WIDTH * BLOCK_SIZE // 2 - 100, GRID_HEIGHT * BLOCK_SIZE // 2))
                self.screen.blit(restart_text, (GRID_WIDTH * BLOCK_SIZE // 2 - 100, GRID_HEIGHT * BLOCK_SIZE // 2 + 50))

            pygame.display.flip()
            self.clock.tick(60)

# Run the game
if __name__ == '__main__':
    game = Tetris()
    game.run()