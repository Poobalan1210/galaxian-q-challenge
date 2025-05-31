"""
Utility functions for the Galaxian game
"""
import pygame
import os

def load_image(path, width=None, height=None):
    """
    Load an image and optionally resize it
    
    Args:
        path (str): Path to the image file
        width (int, optional): Width to resize to
        height (int, optional): Height to resize to
        
    Returns:
        pygame.Surface: The loaded (and possibly resized) image
    """
    try:
        image = pygame.image.load(path).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        raise

def draw_text(surface, text, size, x, y, color):
    """
    Draw text on a surface
    
    Args:
        surface (pygame.Surface): Surface to draw on
        text (str): Text to draw
        size (int): Font size
        x (int): X coordinate (center of text)
        y (int): Y coordinate (top of text)
        color (tuple): RGB color tuple
    """
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def create_assets_directory():
    """
    Create the assets directory if it doesn't exist
    """
    if not os.path.exists('assets'):
        os.makedirs('assets')
        print("Created assets directory. Please add game assets to this folder.")
