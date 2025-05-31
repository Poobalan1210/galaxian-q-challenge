"""
Bullet class for the Galaxian game
"""
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        
        # Create bullet image
        self.image = pygame.Surface((4, 10))
        
        # Color based on direction (player or enemy)
        if speed < 0:  # Player bullet (moving up)
            self.image.fill((0, 255, 255))  # Cyan for player bullets
        else:  # Enemy bullet (moving down)
            self.image.fill((255, 255, 0))  # Yellow for enemy bullets
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed
    
    def update(self):
        # Move the bullet
        self.rect.y += self.speed
        
        # Remove if it goes off screen
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()
