"""
Create basic assets for the Galaxian game
This script generates placeholder images and sounds if you don't have your own assets
"""
import pygame
import os
import sys
import random

def create_player_ship():
    """Create a more detailed player ship image"""
    image = pygame.Surface((50, 40), pygame.SRCALPHA)
    
    # Ship body (improved design)
    pygame.draw.polygon(image, (30, 144, 255), [(25, 0), (5, 30), (45, 30)])
    pygame.draw.polygon(image, (0, 191, 255), [(25, 5), (10, 30), (40, 30)])
    
    # Wings
    pygame.draw.polygon(image, (70, 130, 180), [(5, 30), (0, 40), (20, 40)])
    pygame.draw.polygon(image, (70, 130, 180), [(45, 30), (50, 40), (30, 40)])
    
    # Cockpit
    pygame.draw.circle(image, (173, 216, 230), (25, 20), 8)
    pygame.draw.circle(image, (135, 206, 250), (25, 20), 5)
    
    # Engines
    pygame.draw.rect(image, (255, 140, 0), (10, 35, 10, 5))
    pygame.draw.rect(image, (255, 140, 0), (30, 35, 10, 5))
    pygame.draw.rect(image, (255, 69, 0), (12, 38, 6, 5))
    pygame.draw.rect(image, (255, 69, 0), (32, 38, 6, 5))
    
    return image

def create_enemy_ship(enemy_type):
    """Create more detailed enemy ship images based on type"""
    if enemy_type == 1:  # Medium enemy
        size = (40, 40)
        primary_color = (220, 20, 60)  # Crimson
        secondary_color = (255, 99, 71)  # Tomato
    elif enemy_type == 2:  # Boss enemy
        size = (50, 50)
        primary_color = (139, 0, 0)  # Dark red
        secondary_color = (178, 34, 34)  # Firebrick
    else:  # Basic enemy
        size = (40, 40)
        primary_color = (255, 140, 0)  # Dark orange
        secondary_color = (255, 165, 0)  # Orange
    
    image = pygame.Surface(size, pygame.SRCALPHA)
    
    # Ship body
    if enemy_type == 2:  # Boss - more complex shape
        # Main body
        pygame.draw.polygon(image, primary_color, [
            (25, 0), (5, 15), (0, 30), (10, 40), (40, 40), (50, 30), (45, 15)
        ])
        
        # Secondary body
        pygame.draw.polygon(image, secondary_color, [
            (25, 5), (10, 15), (5, 30), (15, 35), (35, 35), (45, 30), (40, 15)
        ])
        
        # Cockpit
        pygame.draw.circle(image, (255, 215, 0), (25, 20), 10)  # Gold
        pygame.draw.circle(image, (255, 255, 0), (25, 20), 6)   # Yellow
        
        # Wings
        pygame.draw.polygon(image, (169, 169, 169), [(5, 25), (0, 35), (10, 35)])  # Left wing
        pygame.draw.polygon(image, (169, 169, 169), [(45, 25), (50, 35), (40, 35)])  # Right wing
        
        # Engines
        pygame.draw.rect(image, (255, 0, 0), (15, 40, 7, 5))
        pygame.draw.rect(image, (255, 0, 0), (28, 40, 7, 5))
        
    else:  # Regular enemies
        # Main body
        pygame.draw.polygon(image, primary_color, [
            (size[0]//2, 0), (5, size[1]-10), (size[0]-5, size[1]-10)
        ])
        
        # Secondary body
        pygame.draw.polygon(image, secondary_color, [
            (size[0]//2, 5), (10, size[1]-15), (size[0]-10, size[1]-15)
        ])
        
        # Wings
        pygame.draw.polygon(image, (128, 128, 128), [(5, size[1]-15), (0, size[1]), (15, size[1])])
        pygame.draw.polygon(image, (128, 128, 128), [(size[0]-5, size[1]-15), (size[0], size[1]), (size[0]-15, size[1])])
        
        # Cockpit
        pygame.draw.circle(image, (255, 255, 0), (size[0]//2, size[1]//2-5), 6)
        pygame.draw.circle(image, (255, 255, 200), (size[0]//2, size[1]//2-5), 3)
        
        # Engines
        if enemy_type == 1:  # Medium enemy has extra details
            pygame.draw.rect(image, (255, 69, 0), (size[0]//2-8, size[1]-10, 5, 5))
            pygame.draw.rect(image, (255, 69, 0), (size[0]//2+3, size[1]-10, 5, 5))
    
    return image

def create_background():
    """Create a more detailed space background"""
    image = pygame.Surface((800, 600))
    
    # Create a gradient background (dark blue to black)
    for y in range(600):
        # Calculate color based on position (darker at bottom)
        blue_value = max(0, 40 - int(y / 15))
        color = (0, 0, blue_value)
        pygame.draw.line(image, color, (0, y), (799, y))
    
    # Add stars with different sizes and brightness
    for _ in range(300):
        x = random.randint(0, 799)
        y = random.randint(0, 599)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        pygame.draw.circle(image, (brightness, brightness, brightness), (x, y), size)
    
    # Add some brighter stars with glow
    for _ in range(30):
        x = random.randint(0, 799)
        y = random.randint(0, 599)
        # Draw a bright center
        pygame.draw.circle(image, (255, 255, 255), (x, y), 2)
        # Draw a subtle glow
        glow = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 255, 255, 30), (10, 10), 5)
        pygame.draw.circle(glow, (255, 255, 255, 15), (10, 10), 8)
        image.blit(glow, (x-10, y-10))
    
    # Add nebula-like effects with more colors and transparency
    for _ in range(25):
        x = random.randint(0, 799)
        y = random.randint(0, 599)
        size = random.randint(80, 200)
        
        # Choose a color scheme
        color_scheme = random.choice([
            [(75, 0, 130, 20), (138, 43, 226, 10)],  # Purple
            [(139, 0, 0, 20), (255, 69, 0, 10)],     # Red
            [(0, 0, 139, 20), (30, 144, 255, 10)],   # Blue
            [(0, 100, 0, 20), (50, 205, 50, 10)]     # Green
        ])
        
        # Create a surface with per-pixel alpha
        nebula = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw multiple layers with different opacity
        for radius, color in zip([size//2, size//3], color_scheme):
            pygame.draw.circle(nebula, color, (size//2, size//2), radius)
        
        image.blit(nebula, (x-size//2, y-size//2))
    
    # Add a few distant galaxies
    for _ in range(3):
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        size = random.randint(100, 200)
        
        # Create galaxy surface
        galaxy = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw spiral arms
        for i in range(0, 360, 30):
            angle = i * 3.14159 / 180
            for r in range(5, size//2, 2):
                px = int(size/2 + r * pygame.math.Vector2(1, 0).rotate(angle + r/10).x)
                py = int(size/2 + r * pygame.math.Vector2(1, 0).rotate(angle + r/10).y)
                if 0 <= px < size and 0 <= py < size:
                    color = random.choice([
                        (255, 255, 200, 5),  # Yellow
                        (200, 200, 255, 5),  # Blue
                        (255, 200, 200, 5)   # Red
                    ])
                    pygame.draw.circle(galaxy, color, (px, py), 2)
        
        # Draw galaxy core
        pygame.draw.circle(galaxy, (255, 255, 200, 30), (size//2, size//2), size//10)
        
        image.blit(galaxy, (x-size//2, y-size//2))
    
    return image

def create_power_ups():
    """Create power-up images"""
    # Shield power-up
    shield_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    # Draw shield icon
    pygame.draw.circle(shield_img, (0, 100, 255, 180), (15, 15), 14)
    pygame.draw.circle(shield_img, (100, 200, 255, 150), (15, 15), 10)
    pygame.draw.circle(shield_img, (150, 220, 255, 120), (15, 15), 6)
    # Add a glow effect
    for r in range(16, 20):
        pygame.draw.circle(shield_img, (0, 100, 255, 10), (15, 15), r)
    
    # Rocket power-up
    rocket_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    # Draw rocket body
    pygame.draw.rect(rocket_img, (220, 20, 60), (12, 5, 6, 15))
    pygame.draw.polygon(rocket_img, (220, 20, 60), [(12, 5), (15, 0), (18, 5)])
    # Draw fins
    pygame.draw.polygon(rocket_img, (169, 169, 169), [(10, 15), (12, 15), (12, 20)])
    pygame.draw.polygon(rocket_img, (169, 169, 169), [(18, 15), (20, 15), (18, 20)])
    # Draw flame
    pygame.draw.polygon(rocket_img, (255, 165, 0), [(12, 20), (15, 25), (18, 20)])
    pygame.draw.polygon(rocket_img, (255, 215, 0), [(13, 20), (15, 23), (17, 20)])
    # Add a glow effect
    for r in range(16, 20):
        pygame.draw.circle(rocket_img, (255, 100, 0, 10), (15, 15), r)
    
    # Actual rocket projectile
    rocket = pygame.Surface((10, 30), pygame.SRCALPHA)
    # Draw rocket body
    pygame.draw.rect(rocket, (220, 20, 60), (2, 0, 6, 20))
    pygame.draw.polygon(rocket, (220, 20, 60), [(2, 0), (5, -5), (8, 0)])
    # Draw fins
    pygame.draw.polygon(rocket, (169, 169, 169), [(0, 15), (2, 15), (2, 20)])
    pygame.draw.polygon(rocket, (169, 169, 169), [(8, 15), (10, 15), (8, 20)])
    # Draw flame
    pygame.draw.polygon(rocket, (255, 165, 0), [(2, 20), (5, 30), (8, 20)])
    pygame.draw.polygon(rocket, (255, 215, 0), [(3, 20), (5, 25), (7, 20)])
    
    return shield_img, rocket_img, rocket

def create_shield_effect():
    """Create shield effect for player"""
    shield = pygame.Surface((70, 60), pygame.SRCALPHA)
    
    # Draw shield bubble
    pygame.draw.ellipse(shield, (0, 100, 255, 80), (0, 0, 70, 60))
    pygame.draw.ellipse(shield, (100, 200, 255, 40), (5, 5, 60, 50))
    
    # Add highlight
    pygame.draw.arc(shield, (255, 255, 255, 100), (5, 5, 60, 50), 0.5, 2.5, 3)
    
    return shield

def create_laser_sound():
    """Create a simple laser sound effect"""
    pygame.mixer.init()
    sound = pygame.mixer.Sound(buffer=bytes([128] * 4000))
    return sound

def create_explosion_sound():
    """Create a simple explosion sound effect"""
    pygame.mixer.init()
    sound = pygame.mixer.Sound(buffer=bytes([random_byte() for _ in range(8000)]))
    return sound

def random_byte():
    """Generate a random byte for sound effects"""
    return random.randint(0, 255)

def main():
    """Create all assets"""
    pygame.init()
    
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Create and save player ship
    player_ship = create_player_ship()
    pygame.image.save(player_ship, 'assets/player_ship.png')
    
    # Create and save enemy ships
    for i in range(3):
        enemy_ship = create_enemy_ship(i)
        pygame.image.save(enemy_ship, f'assets/enemy{i+1}.png')
    
    # Create and save background
    background = create_background()
    pygame.image.save(background, 'assets/background.png')
    
    # Create and save power-ups
    shield_powerup, rocket_powerup, rocket = create_power_ups()
    pygame.image.save(shield_powerup, 'assets/shield_powerup.png')
    pygame.image.save(rocket_powerup, 'assets/rocket_powerup.png')
    pygame.image.save(rocket, 'assets/rocket.png')
    
    # Create and save shield effect
    shield_effect = create_shield_effect()
    pygame.image.save(shield_effect, 'assets/shield_effect.png')
    
    # Create and save sound effects
    laser_sound = create_laser_sound()
    explosion_sound = create_explosion_sound()
    # pygame.mixer.Sound objects don't have a save method
    # We'll use a different approach or skip this for now
    print("Sound files would need to be created separately")
    
    print("All assets created successfully!")
    pygame.quit()

if __name__ == "__main__":
    main()
