"""
Power-up classes for the Galaxian game
"""
import pygame
import random
from game_utils import load_image

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        pygame.sprite.Sprite.__init__(self)
        
        self.powerup_type = powerup_type
        
        # Create more visible power-up images
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        if powerup_type == "shield":
            # Blue shield icon with glow effect
            pygame.draw.circle(self.image, (0, 100, 255), (15, 15), 15)
            pygame.draw.circle(self.image, (100, 200, 255), (15, 15), 10)
            pygame.draw.circle(self.image, (200, 230, 255), (15, 15), 5)
            # Add pulsating effect
            self.glow_size = 15
            self.glow_direction = 1
        else:  # rocket
            # Red rocket icon with more detail
            pygame.draw.rect(self.image, (255, 50, 50), (10, 5, 10, 20))
            pygame.draw.polygon(self.image, (255, 100, 50), [(10, 5), (15, 0), (20, 5)])
            pygame.draw.rect(self.image, (150, 150, 150), (8, 25, 14, 5))
            # Add flame effect
            pygame.draw.polygon(self.image, (255, 215, 0), [(12, 25), (15, 30), (18, 25)])
            # Add pulsating effect
            self.glow_size = 15
            self.glow_direction = 1
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement speed
        self.speed = 3
        
        # Sound effect
        try:
            self.pickup_sound = pygame.mixer.Sound('assets/powerup.wav')
            self.pickup_sound.set_volume(0.4)
        except:
            self.pickup_sound = None
    
    def update(self):
        # Move downward
        self.rect.y += self.speed
        
        # Add pulsating glow effect
        self.glow_size += 0.2 * self.glow_direction
        if self.glow_size > 18:
            self.glow_direction = -1
        elif self.glow_size < 12:
            self.glow_direction = 1
        
        # Remove if it goes off screen
        if self.rect.top > 600:
            self.kill()
    
    def apply(self, player, game_state):
        """Apply power-up effect to player"""
        if self.pickup_sound:
            self.pickup_sound.play()
            
        if self.powerup_type == "shield":
            player.activate_shield()
            game_state.score += 50
        elif self.powerup_type == "rocket":
            player.fire_rocket()
            game_state.score += 100
        
        self.kill()


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Create rocket image
        try:
            self.image = load_image('assets/rocket.png', 10, 30)
        except:
            self.image = pygame.Surface((10, 30), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 50, 50), (0, 0, 10, 20))
            pygame.draw.polygon(self.image, (255, 200, 0), [(0, 20), (5, 30), (10, 20)])
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        # Movement speed
        self.speed = -8  # Faster than regular bullets
        
        # Explosion radius
        self.explosion_radius = 100
        
        # Sound effect
        try:
            self.launch_sound = pygame.mixer.Sound('assets/rocket_launch.wav')
            self.launch_sound.set_volume(0.5)
            self.launch_sound.play()
        except:
            pass
    
    def update(self):
        # Move upward
        self.rect.y += self.speed
        
        # Remove if it goes off screen
        if self.rect.bottom < 0:
            self.kill()
    
    def explode(self):
        """Return the center point for explosion effect"""
        return self.rect.center
