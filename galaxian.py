#!/usr/bin/env python3
"""
Galaxian Game - A space-themed fixed shooter game
"""
import pygame
import sys
import random
from pygame.locals import *

# Import game components
from player import Player
from enemy import Enemy, EnemyFleet
from bullet import Bullet
from explosion import Explosion, RocketExplosion
from powerup import PowerUp, Rocket
from game_utils import load_image, draw_text

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaxian")

# Load background image
try:
    background = load_image('assets/background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
except:
    # Fallback to a black background if image loading fails
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK)

# Game state
class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.paused = False

def main():
    # Clock for controlling game speed
    clock = pygame.time.Clock()
    
    # Game state
    game_state = GameState()
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    rockets = pygame.sprite.Group()
    
    # Create player
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(player)
    
    # Add initial powerups for testing
    shield_powerup = PowerUp(SCREEN_WIDTH // 3, 100, "shield")
    rocket_powerup = PowerUp(2 * SCREEN_WIDTH // 3, 100, "rocket")
    all_sprites.add(shield_powerup)
    all_sprites.add(rocket_powerup)
    powerups.add(shield_powerup)
    powerups.add(rocket_powerup)
    
    # Create enemy fleet
    enemy_fleet = EnemyFleet(SCREEN_WIDTH, game_state.level)
    for enemy in enemy_fleet.enemies:
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Main game loop
    running = True
    while running:
        # Keep the game running at the right speed
        clock.tick(FPS)
        
        # Process input/events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_p:
                    game_state.paused = not game_state.paused
                elif event.key == K_SPACE and not game_state.paused and not game_state.game_over:
                    bullet = player.shoot()
                    if bullet:
                        all_sprites.add(bullet)
                        player_bullets.add(bullet)
        
        # Skip updates if game is paused
        if game_state.paused:
            # Draw everything
            screen.blit(background, (0, 0))
            all_sprites.draw(screen)
            player.draw(screen)  # Draw player with shield if active
            draw_text(screen, "PAUSED", 64, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, WHITE)
            draw_text(screen, f"Score: {game_state.score}", 22, SCREEN_WIDTH//2, 10, WHITE)
            draw_text(screen, f"Lives: {game_state.lives}", 22, 50, 10, WHITE)
            draw_text(screen, f"Level: {game_state.level}", 22, SCREEN_WIDTH-50, 10, WHITE)
            pygame.display.flip()
            continue
            
        if game_state.game_over:
            # Draw game over screen
            screen.blit(background, (0, 0))
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, RED)
            draw_text(screen, f"Final Score: {game_state.score}", 36, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70, WHITE)
            draw_text(screen, "Press ESC to exit", 22, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120, WHITE)
            pygame.display.flip()
            continue
        
        # Update all game objects
        all_sprites.update()
        
        # Enemy shooting logic
        for enemy in enemies:
            if random.random() < 0.005 * game_state.level:  # Chance increases with level
                bullet = enemy.shoot()
                if bullet:
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet)
        
        # Random power-up spawning (increased probability)
        if random.random() < 0.01 * game_state.level:  # Much higher chance (10x more frequent)
            powerup_type = random.choice(["shield", "rocket"])
            x = random.randint(50, SCREEN_WIDTH - 50)
            powerup = PowerUp(x, 0, powerup_type)
            all_sprites.add(powerup)
            powerups.add(powerup)
        
        # Check for collisions between player bullets and enemies
        hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
        for hit in hits:
            game_state.score += 100
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosions.add(explosion)
        
        # Check for collisions between rockets and enemies
        hits = pygame.sprite.groupcollide(enemies, rockets, False, True)
        for enemy, rocket_list in hits.items():
            for rocket in rocket_list:
                # Create rocket explosion
                explosion = RocketExplosion(rocket.explode())
                all_sprites.add(explosion)
                explosions.add(explosion)
                
                # Damage all enemies within explosion radius
                for target in enemies:
                    # Calculate distance between explosion and enemy
                    distance = pygame.math.Vector2(target.rect.center).distance_to(
                        pygame.math.Vector2(explosion.rect.center))
                    
                    if distance < explosion.size / 2:  # If within explosion radius
                        target.kill()
                        game_state.score += 100
                        # Create smaller explosion for each affected enemy
                        small_explosion = Explosion(target.rect.center)
                        all_sprites.add(small_explosion)
                        explosions.add(small_explosion)
        
        # Check for collisions between enemy bullets and player
        if not player.is_shielded():  # Only check if shield is not active
            hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
            if hits:
                game_state.lives -= 1
                explosion = Explosion(player.rect.center)
                all_sprites.add(explosion)
                explosions.add(explosion)
                player.reset_position()
                if game_state.lives <= 0:
                    game_state.game_over = True
        else:
            # If shield is active, destroy enemy bullets that hit the shield
            hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        
        # Check for direct collisions between player and enemies
        if not player.is_shielded():  # Only check if shield is not active
            hits = pygame.sprite.spritecollide(player, enemies, True)
            if hits:
                game_state.lives -= 1
                explosion = Explosion(player.rect.center)
                all_sprites.add(explosion)
                explosions.add(explosion)
                player.reset_position()
                if game_state.lives <= 0:
                    game_state.game_over = True
        else:
            # If shield is active, destroy enemies that hit the shield
            hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in hits:
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)
                explosions.add(explosion)
                game_state.score += 50
        
        # Check for collisions between player and power-ups
        hits = pygame.sprite.spritecollide(player, powerups, False)
        for hit in hits:
            if hit.powerup_type == "shield":
                player.activate_shield()
                hit.apply(player, game_state)
            elif hit.powerup_type == "rocket":
                rocket = player.fire_rocket()
                all_sprites.add(rocket)
                rockets.add(rocket)
                hit.apply(player, game_state)
        
        # If all enemies are destroyed, advance to next level
        if len(enemies) == 0:
            game_state.level += 1
            enemy_fleet = EnemyFleet(SCREEN_WIDTH, game_state.level)
            for enemy in enemy_fleet.enemies:
                all_sprites.add(enemy)
                enemies.add(enemy)
        
        # Draw everything
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        player.draw(screen)  # Draw player with shield if active
        
        # Draw HUD
        draw_text(screen, f"Score: {game_state.score}", 22, SCREEN_WIDTH//2, 10, WHITE)
        draw_text(screen, f"Lives: {game_state.lives}", 22, 50, 10, WHITE)
        draw_text(screen, f"Level: {game_state.level}", 22, SCREEN_WIDTH-50, 10, WHITE)
        
        # Show shield timer if active
        if player.shield_active:
            shield_time_left = (player.shield_duration - (pygame.time.get_ticks() - player.shield_time)) // 1000
            draw_text(screen, f"Shield: {shield_time_left}s", 18, 150, 10, (100, 200, 255))
        
        # Flip the display
        pygame.display.flip()
    
    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
