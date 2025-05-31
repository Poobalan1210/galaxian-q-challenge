"""
Player class for the Galaxian game
"""
import pygame
from pygame.locals import *
import random
from bullet import Bullet
from powerup import Rocket
from game_utils import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        
        # Load player ship image
        try:
            self.image = load_image('assets/player_ship.png', 50, 40)
        except:
            # Fallback to a simple shape if image loading fails
            self.image = pygame.Surface((50, 40))
            self.image.fill((0, 255, 0))
            pygame.draw.polygon(self.image, (255, 255, 255), 
                               [(25, 0), (0, 40), (50, 40)])
        
        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()
        
        # Set initial position at the bottom center of the screen
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        
        # Movement speed
        self.speed = 8
        
        # Screen boundaries
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Shooting cooldown
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        
        # Shield properties
        self.shield_active = False
        self.shield_time = 0
        self.shield_duration = 30000  # 30 seconds in milliseconds
        
        # Create a more visible shield effect
        self.shield_image = pygame.Surface((70, 60), pygame.SRCALPHA)
        # Draw shield bubble with bright blue color
        pygame.draw.ellipse(self.shield_image, (0, 150, 255, 120), (0, 0, 70, 60))
        pygame.draw.ellipse(self.shield_image, (100, 200, 255, 80), (5, 5, 60, 50))
        # Add highlight
        pygame.draw.arc(self.shield_image, (255, 255, 255, 150), (5, 5, 60, 50), 0.5, 2.5, 3)
        
        # Sound effects
        try:
            self.shoot_sound = pygame.mixer.Sound('assets/laser.wav')
            self.shoot_sound.set_volume(0.4)
            self.shield_sound = pygame.mixer.Sound('assets/shield.wav')
            self.shield_sound.set_volume(0.5)
            self.rocket_sound = pygame.mixer.Sound('assets/rocket_launch.wav')
            self.rocket_sound.set_volume(0.6)
        except:
            self.shoot_sound = None
            self.shield_sound = None
            self.rocket_sound = None
    
    def update(self):
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Move left/right
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed
        
        # Keep player on screen
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        
        # Update shield if active
        if self.shield_active:
            now = pygame.time.get_ticks()
            if now - self.shield_time > self.shield_duration:
                self.shield_active = False
    
    def draw(self, surface):
        # Draw the player ship
        surface.blit(self.image, self.rect)
        
        # Draw shield if active
        if self.shield_active:
            # Create a more visible shield effect
            shield_rect = self.shield_image.get_rect()
            shield_rect.center = self.rect.center
            
            # Add pulsating effect to make shield more visible
            now = pygame.time.get_ticks()
            pulse = (now % 1000) / 1000  # Value between 0 and 1
            
            # Create a copy of the shield image with varying opacity
            shield_copy = self.shield_image.copy()
            if pulse > 0.5:
                alpha = int(200 + 55 * (pulse - 0.5) * 2)  # 200-255
            else:
                alpha = int(200 - 55 * pulse * 2)  # 145-200
            
            shield_copy.set_alpha(alpha)
            surface.blit(shield_copy, shield_rect)
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, -10)  # -10 for upward movement
            
            # Play sound if available
            if self.shoot_sound:
                self.shoot_sound.play()
                
            return bullet
        return None
    
    def fire_rocket(self):
        """Fire a rocket that explodes and damages enemies in an area"""
        # Create a more visible rocket
        rocket_img = pygame.Surface((10, 30), pygame.SRCALPHA)
        # Draw rocket body
        pygame.draw.rect(rocket_img, (220, 20, 60), (2, 0, 6, 20))
        pygame.draw.polygon(rocket_img, (220, 20, 60), [(2, 0), (5, -5), (8, 0)])
        # Draw fins
        pygame.draw.polygon(rocket_img, (169, 169, 169), [(0, 15), (2, 15), (2, 20)])
        pygame.draw.polygon(rocket_img, (169, 169, 169), [(8, 15), (10, 15), (8, 20)])
        # Draw flame
        pygame.draw.polygon(rocket_img, (255, 165, 0), [(2, 20), (5, 30), (8, 20)])
        pygame.draw.polygon(rocket_img, (255, 215, 0), [(3, 20), (5, 25), (7, 20)])
        
        rocket = Rocket(self.rect.centerx, self.rect.top)
        rocket.image = rocket_img  # Replace with our custom image
        
        # Play sound if available
        if self.rocket_sound:
            self.rocket_sound.play()
            
        return rocket
    
    def activate_shield(self):
        """Activate shield for protection"""
        self.shield_active = True
        self.shield_time = pygame.time.get_ticks()
        
        # Play sound if available
        if self.shield_sound:
            self.shield_sound.play()
    
    def is_shielded(self):
        """Check if shield is active"""
        return self.shield_active
    
    def reset_position(self):
        """Reset player position after being hit"""
        self.rect.centerx = self.screen_width // 2
        self.rect.bottom = self.screen_height - 10
