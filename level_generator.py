import random
import math

class LevelGenerator:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.difficulty = 1
        
    def generate_level(self, level_number):
        """Generate a level configuration based on the level number"""
        # Increase difficulty with each level
        self.difficulty = 1 + (level_number * 0.2)
        
        level_data = {
            'enemy_count': self._calculate_enemy_count(level_number),
            'enemy_types': self._determine_enemy_types(level_number),
            'formation': self._generate_formation(level_number),
            'attack_patterns': self._generate_attack_patterns(level_number),
            'speed_multiplier': min(1 + (level_number * 0.1), 2.5),  # Cap at 2.5x speed
            'dive_frequency': min(0.002 + (level_number * 0.0005), 0.01),  # Cap at 1% chance per frame
            'special_events': self._generate_special_events(level_number)
        }
        
        return level_data
    
    def _calculate_enemy_count(self, level_number):
        """Calculate how many enemies should appear in this level"""
        base_count = 20
        additional = min(level_number * 3, 30)  # Add more enemies per level, max +30
        return base_count + additional
    
    def _determine_enemy_types(self, level_number):
        """Determine what types of enemies should appear and their ratios"""
        enemy_types = {
            'basic': 0.7 - (level_number * 0.05),  # Decrease basic enemies as levels progress
            'diver': 0.2 + (level_number * 0.02),  # Increase divers
            'bomber': 0.1 + (level_number * 0.01),  # Increase bombers
            'elite': 0 if level_number < 3 else 0.05 + ((level_number - 3) * 0.01)  # Elite enemies appear from level 3
        }
        
        # Normalize percentages to ensure they sum to 1
        total = sum(enemy_types.values())
        for key in enemy_types:
            enemy_types[key] = max(0, enemy_types[key] / total)
            
        return enemy_types
    
    def _generate_formation(self, level_number):
        """Generate enemy formation pattern"""
        formations = [
            'standard_grid',  # Classic Galaxian grid
            'v_formation',    # V-shaped formation
            'circle',         # Circular formation
            'diamond',        # Diamond pattern
            'wave'            # Wave pattern
        ]
        
        # More complex formations become available at higher levels
        available_formations = formations[:1 + min(level_number, len(formations) - 1)]
        
        # Choose a random formation from available ones
        formation_type = random.choice(available_formations)
        
        # Generate formation parameters
        if formation_type == 'standard_grid':
            rows = min(3 + math.floor(level_number / 3), 6)
            cols = min(8 + math.floor(level_number / 2), 12)
            return {
                'type': formation_type,
                'rows': rows,
                'cols': cols,
                'spacing_x': 50,
                'spacing_y': 40,
                'offset_x': (self.screen_width - (cols * 50)) / 2,
                'offset_y': 60
            }
        elif formation_type == 'v_formation':
            size = min(5 + level_number, 15)
            return {
                'type': formation_type,
                'size': size,
                'spacing': 40,
                'offset_x': self.screen_width / 2,
                'offset_y': 80
            }
        elif formation_type == 'circle':
            radius = min(100 + (level_number * 10), 180)
            count = min(12 + level_number, 24)
            return {
                'type': formation_type,
                'radius': radius,
                'count': count,
                'center_x': self.screen_width / 2,
                'center_y': 150
            }
        elif formation_type == 'diamond':
            size = min(3 + math.floor(level_number / 2), 7)
            return {
                'type': formation_type,
                'size': size,
                'spacing': 50,
                'offset_x': self.screen_width / 2,
                'offset_y': 100
            }
        else:  # wave
            width = min(6 + level_number, 15)
            height = min(2 + math.floor(level_number / 3), 5)
            return {
                'type': formation_type,
                'width': width,
                'height': height,
                'spacing_x': 50,
                'spacing_y': 40,
                'offset_x': (self.screen_width - (width * 50)) / 2,
                'offset_y': 60
            }
    
    def _generate_attack_patterns(self, level_number):
        """Generate attack patterns for enemies"""
        patterns = [
            'straight_dive',      # Classic straight dive
            'curved_dive',        # Curved diving path
            'swoop_and_return',   # Swoop down and return to formation
            'spiral_attack',      # Spiral attack pattern
            'coordinated_dive'    # Multiple enemies dive together
        ]
        
        # More complex attack patterns become available at higher levels
        available_patterns = patterns[:1 + min(level_number, len(patterns) - 1)]
        
        # Select 1-3 patterns for this level
        num_patterns = min(1 + math.floor(level_number / 3), 3)
        selected_patterns = random.sample(available_patterns, min(num_patterns, len(available_patterns)))
        
        return selected_patterns
    
    def _generate_special_events(self, level_number):
        """Generate special events for this level"""
        events = []
        
        # Asteroid field (from level 2)
        if level_number >= 2 and random.random() < 0.3:
            events.append({
                'type': 'asteroid_field',
                'density': min(0.1 + (level_number * 0.02), 0.3),  # 10-30% density
                'speed': 1 + (level_number * 0.2)
            })
        
        # Boss enemy (every 5 levels)
        if level_number % 5 == 0:
            events.append({
                'type': 'boss',
                'health': 10 + (level_number * 2),
                'attack_pattern': random.choice(['sweep', 'barrage', 'minions'])
            })
        
        # Wormhole (from level 4)
        if level_number >= 4 and random.random() < 0.2:
            events.append({
                'type': 'wormhole',
                'duration': 15,  # seconds
                'position': (random.randint(100, self.screen_width - 100), 
                             random.randint(100, self.screen_height // 2))
            })
            
        return events
