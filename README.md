# Galaxian Game

A space-themed fixed shooter game inspired by the classic arcade game Galaxian, implemented in Python using Pygame.

## Description

In this game, you control a spaceship at the bottom of the screen and must defend against waves of alien invaders. The aliens move in formation and occasionally dive down to attack you directly. As you progress through levels, the game becomes increasingly challenging with more enemies, faster movement, and new attack patterns.

## Features

- **Player-controlled spaceship** with responsive movement and shooting capabilities
- **Multiple enemy types** with different behaviors:
  - Basic enemies that move in formation
  - Medium enemies with increased health and speed
  - Boss enemies that appear every 5 levels
  - Enemies that dive down to attack the player directly
- **Power-up system** with special abilities:
  - Shield power-up for temporary invulnerability (30 seconds duration)
  - Rocket power-up that creates area-of-effect explosions
- **Dynamic difficulty progression**:
  - Increasing number of enemies per level
  - Faster enemy movement and more aggressive diving
  - More complex enemy formations and attack patterns
- **Visual effects**:
  - Detailed explosion animations with particle effects
  - Shield visual effects with pulsating glow
  - Rocket trails and explosions with dynamic lighting
- **Game mechanics**:
  - Score tracking system (100 points per enemy, 50 points for shielded collisions)
  - Lives system with respawn functionality (3 lives by default)
  - Level progression with increasing challenge
  - Pause functionality
- **Advanced level generation** with different enemy formations:
  - Standard grid formations (classic Galaxian style)
  - V-shaped formations (available at higher levels)
  - Circular formations (available at higher levels)
  - Diamond patterns (available at higher levels)
  - Wave patterns (available at higher levels)
- **Special events** (at higher levels):
  - Asteroid fields with varying density
  - Boss enemies every 5 levels
  - Wormholes that affect gameplay

## How to Play

1. Install the required dependencies:
   ```
   pip install pygame
   ```

2. Run the game:
   ```
   python galaxian.py
   ```

3. Controls:
   - Left/Right Arrow Keys or A/D: Move the ship
   - Space: Shoot
   - P: Pause the game
   - ESC: Quit

## Game Objectives

- Destroy enemy ships to earn points (100 points per standard enemy)
- Collect power-ups to gain advantages:
  - Shield: Provides temporary invulnerability for 30 seconds
  - Rocket: Fires a rocket that explodes and damages multiple enemies in an area
- Survive as long as possible and achieve the highest score
- Progress through increasingly difficult levels with new enemy formations and behaviors

## Setup

Before running the game for the first time, you can generate placeholder assets by running:
```
python assets_creator.py
```

This will create basic graphics and sound effects. You can replace these with your own assets by placing them in the `assets` directory.

## Project Structure

- `galaxian.py`: Main game file with game loop and core mechanics
- `player.py`: Player ship class with movement, shooting, and shield functionality
- `enemy.py`: Enemy ships and fleet classes with different behaviors and attack patterns
- `bullet.py`: Projectile class for both player and enemy bullets
- `explosion.py`: Explosion animation classes with particle effects
- `powerup.py`: Power-up classes including shield and rocket power-ups
- `game_utils.py`: Utility functions for loading assets and drawing text
- `level_generator.py`: Advanced level generation with different enemy formations
- `assets_creator.py`: Script to generate placeholder assets
- `assets/`: Directory containing game graphics and sound effects

## Technical Details

- Built with Python 3 and Pygame
- Object-oriented design with separate classes for game entities
- Collision detection for gameplay interactions
- Dynamic difficulty scaling based on player progress
- Particle system for visual effects
- Screen resolution: 800x600 pixels
- Frame rate: 60 FPS