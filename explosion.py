"""
Explosion animation class for the Galaxian game
"""
import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size=None, is_rocket=False):
        pygame.sprite.Sprite.__init__(self)
        
        # Set explosion size
        if size is None:
            self.size = random.randint(20, 40)
        else:
            self.size = size
            
        self.is_rocket = is_rocket
        
        # Create initial explosion frame
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        if self.is_rocket:
            # Rocket explosions are larger and more colorful
            color = (255, 255, 255)
        else:
            color = (255, 255, 255)
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # Animation parameters
        self.frame = 0
        self.frame_rate = 50  # milliseconds per frame
        self.last_update = pygame.time.get_ticks()
        self.frame_count = 12 if self.is_rocket else 8  # More frames for rocket explosions
        
        # Sound effect
        try:
            if self.is_rocket:
                self.explosion_sound = pygame.mixer.Sound('assets/big_explosion.wav')
                self.explosion_sound.set_volume(0.5)
            else:
                self.explosion_sound = pygame.mixer.Sound('assets/explosion.wav')
                self.explosion_sound.set_volume(0.3)
            self.explosion_sound.play()
        except:
            pass
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            
            if self.frame >= self.frame_count:
                self.kill()  # Remove explosion when animation is complete
            else:
                # Create new explosion frame
                old_center = self.rect.center
                self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                
                # Different colors for different frames
                if self.is_rocket:
                    # Rocket explosion colors
                    if self.frame < 3:
                        color = (255, 255, 255)  # White
                    elif self.frame < 6:
                        color = (255, 255, 0)    # Yellow
                    elif self.frame < 9:
                        color = (255, 165, 0)    # Orange
                    else:
                        color = (255, 69, 0)     # Red-Orange
                        
                    # Draw more particles for rocket explosions
                    particles = 25
                    max_radius = 5
                else:
                    # Regular explosion colors
                    if self.frame < 3:
                        color = (255, 255, 255)  # White
                    elif self.frame < 5:
                        color = (255, 255, 0)    # Yellow
                    else:
                        color = (255, 165, 0)    # Orange
                        
                    particles = 15
                    max_radius = 3
                
                # Draw explosion particles
                for _ in range(particles):
                    # Calculate position based on frame (expanding outward)
                    distance = (self.frame / self.frame_count) * (self.size / 2)
                    angle = random.uniform(0, 360)
                    dx = distance * pygame.math.Vector2(1, 0).rotate(angle).x
                    dy = distance * pygame.math.Vector2(1, 0).rotate(angle).y
                    
                    x = int(self.size / 2 + dx)
                    y = int(self.size / 2 + dy)
                    
                    # Keep within bounds
                    x = max(0, min(x, self.size - 1))
                    y = max(0, min(y, self.size - 1))
                    
                    radius = random.randint(1, max_radius)
                    pygame.draw.circle(self.image, color, (x, y), radius)
                
                # Add a glow effect for rocket explosions
                if self.is_rocket:
                    glow_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                    glow_radius = int(self.size / 2 * (self.frame / self.frame_count))
                    pygame.draw.circle(glow_surface, (255, 165, 0, 50), 
                                      (self.size // 2, self.size // 2), glow_radius)
                    self.image.blit(glow_surface, (0, 0))
                
                # Make black background transparent
                self.image.set_colorkey((0, 0, 0))
                
                # Keep the explosion centered
                self.rect = self.image.get_rect()
                self.rect.center = old_center


class RocketExplosion(Explosion):
    """Special explosion for rockets with larger area effect"""
    def __init__(self, center):
        super().__init__(center, size=100, is_rocket=True)
