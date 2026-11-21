import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Defender")

# Colors
BLACK = (10, 10, 20)
CYAN = (0, 255, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Frame rate setup
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Consolas", 30)
large_font = pygame.font.SysFont("Consolas", 60)

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main():
    # Player attributes
    player_size = 40
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 20
    player_speed = 7

    # Bullet attributes
    bullets = []
    bullet_width = 6
    bullet_height = 15
    bullet_speed = 10

    # Enemy attributes
    enemies = []
    enemy_size = 40
    enemy_speed = 3
    spawn_rate = 40  # Lower number = faster spawning
    frame_count = 0

    score = 0
    game_over = False

    # Main game loop
    while True:
        screen.fill(BLACK)
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    # Shoot a bullet
                    bullets.append(pygame.Rect(
                        player_x + player_size // 2 - bullet_width // 2, 
                        player_y, 
                        bullet_width, 
                        bullet_height
                    ))
                if event.key == pygame.K_r and game_over:
                    # Restart the game by calling main() again
                    main()
                if event.key == pygame.K_q and game_over:
                    pygame.quit()
                    sys.exit()

        # 2. Game Logic
        if not game_over:
            # Player Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
                player_x += player_speed

            # Update Bullets
            for bullet in bullets[:]:
                bullet.y -= bullet_speed
                if bullet.y < 0:  # Remove bullet if it goes off-screen
                    bullets.remove(bullet)

            # Spawn Enemies
            frame_count += 1
            if frame_count >= spawn_rate:
                enemy_x = random.randint(0, WIDTH - enemy_size)
                enemies.append(pygame.Rect(enemy_x, -enemy_size, enemy_size, enemy_size))
                frame_count = 0
                
                # Slowly increase difficulty by reducing spawn timer
                if spawn_rate > 15:
                    spawn_rate -= 0.2

            # Update Enemies & Check Collisions
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            
            for enemy in enemies[:]:
                enemy.y += enemy_speed
                
                # If enemy passes the player, subtract points
                if enemy.y > HEIGHT:
                    enemies.remove(enemy)
                    score -= 5  

                # If enemy hits the player -> Game Over
                if enemy.colliderect(player_rect):
                    game_over = True

                # Check if any bullet hits this enemy
                for bullet in bullets[:]:
                    if enemy.colliderect(bullet):
                        if enemy in enemies: enemies.remove(enemy)
                        if bullet in bullets: bullets.remove(bullet)
                        score += 10

        # 3. Drawing to Screen
        # Draw Player (Cyan Square)
        pygame.draw.rect(screen, CYAN, (player_x, player_y, player_size, player_size))
        
        # Draw Bullets (Yellow Rectangles)
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)
            
        # Draw Enemies (Red Squares)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Draw UI
        draw_text(f"Score: {score}", font, WHITE, screen, 100, 30)

        if game_over:
            draw_text("GAME OVER", large_font, RED, screen, WIDTH//2, HEIGHT//2 - 50)
            draw_text("Press 'R' to Restart or 'Q' to Quit", font, WHITE, screen, WIDTH//2, HEIGHT//2 + 20)

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()