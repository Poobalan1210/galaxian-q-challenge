"""
Enemy classes for the Galaxian game
"""
import pygame
import random
from bullet import Bullet
from game_utils import load_image

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type=0):
        pygame.sprite.Sprite.__init__(self)
        
        # Different enemy types
        self.enemy_type = enemy_type
        
        # Load enemy ship image based on type
        try:
            if enemy_type == 0:  # Basic enemy
                self.image = load_image('assets/enemy1.png', 40, 40)
            elif enemy_type == 1:  # Medium enemy
                self.image = load_image('assets/enemy2.png', 40, 40)
            else:  # Boss enemy
                self.image = load_image('assets/enemy3.png', 50, 50)
        except:
            # Fallback to simple shapes if image loading fails
            if enemy_type == 2:  # Boss
                self.image = pygame.Surface((50, 50))
                self.image.fill((255, 0, 0))
            else:
                self.image = pygame.Surface((40, 40))
                self.image.fill((255, 0, 0) if enemy_type == 1 else (255, 165, 0))
            
            # Draw a simple alien shape
            pygame.draw.polygon(self.image, (255, 255, 255), 
                               [(self.image.get_width()//2, 0), 
                                (0, self.image.get_height()), 
                                (self.image.get_width(), self.image.get_height())])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement parameters
        self.speed_x = random.choice([-1, 1]) * (2 + enemy_type)
        self.speed_y = 0
        self.dive_chance = 0.001 * (enemy_type + 1)  # Higher chance for stronger enemies
        self.diving = False
        self.original_y = y
        
        # Shooting parameters
        self.shoot_chance = 0.002 * (enemy_type + 1)  # Higher chance for stronger enemies
    
    def update(self):
        # Regular movement
        if not self.diving:
            self.rect.x += self.speed_x
            
            # Random chance to start diving
            if random.random() < self.dive_chance:
                self.diving = True
                self.speed_y = 5 + self.enemy_type
                self.dive_target_x = random.randint(50, 750)  # Random x position to dive towards
        else:
            # Diving behavior
            self.rect.y += self.speed_y
            
            # Move towards dive target
            if self.rect.x < self.dive_target_x:
                self.rect.x += 3
            elif self.rect.x > self.dive_target_x:
                self.rect.x -= 3
            
            # Return to formation after diving past bottom of screen
            if self.rect.top > 600:
                self.rect.y = self.original_y - 600  # Reappear at top
                self.diving = False
                self.speed_y = 0
        
        # Change direction when hitting screen edges
        if self.rect.right > 800 or self.rect.left < 0:
            self.speed_x *= -1
    
    def shoot(self):
        # Only shoot if not diving
        if not self.diving:
            return Bullet(self.rect.centerx, self.rect.bottom, 5)  # 5 for downward movement
        return None


class EnemyFleet:
    def __init__(self, screen_width, level):
        self.enemies = []
        
        # Adjust difficulty based on level
        rows = min(3 + level // 2, 6)  # More rows as level increases, max 6
        cols = min(6 + level // 3, 10)  # More columns as level increases, max 10
        
        # Create enemy formation
        for row in range(rows):
            for col in range(cols):
                # Determine enemy type based on row
                if row == 0 and col == cols // 2 and level > 2:
                    enemy_type = 2  # Boss in the middle of first row on higher levels
                elif row == 0:
                    enemy_type = 1  # Medium enemies in first row
                else:
                    enemy_type = 0  # Basic enemies in other rows
                
                # Calculate position
                x = 100 + col * 60
                y = 50 + row * 50
                
                # Create enemy
                enemy = Enemy(x, y, enemy_type)
                self.enemies.append(enemy)
