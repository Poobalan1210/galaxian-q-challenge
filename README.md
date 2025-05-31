# Galaxian Game

A space-themed fixed shooter game inspired by the classic arcade game Galaxian, implemented in Python using Pygame.

## Description

In this game, you control a spaceship at the bottom of the screen and must defend against waves of alien invaders. The aliens will move in formation and occasionally dive down to attack you directly.

## Features

- Player-controlled spaceship with shooting capability
- Multiple types of enemy ships with different behaviors
- Increasing difficulty with each level
- Score tracking and lives system
- Explosion animations and sound effects

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

## Setup

Before running the game for the first time, you can generate placeholder assets by running:
```
python assets_creator.py
```

This will create basic graphics and sound effects. You can replace these with your own assets by placing them in the `assets` directory.

## Files

- `galaxian.py`: Main game file
- `player.py`: Player ship class
- `enemy.py`: Enemy ships and fleet classes
- `bullet.py`: Projectile class
- `explosion.py`: Explosion animation class
- `game_utils.py`: Utility functions
- `assets_creator.py`: Script to generate placeholder assets