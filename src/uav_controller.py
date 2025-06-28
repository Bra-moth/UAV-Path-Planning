"""
UAV Controller for Path Planning Demo
Simplified UAV control and path planning for demonstration purposes
"""

import math
import random
from typing import List, Tuple, Optional
from bird_simulation import Bird

class UAVController:
    """Simplified UAV controller for demo purposes"""
    
    def __init__(self, position: Tuple[int, int]):
        self.position = list(position)
        self.velocity = [0, 0]
        self.energy = 100.0
        self.max_speed = 8.0
        self.target_bird: Optional[Bird] = None
        self.target_position: Optional[Tuple[int, int]] = None
        self.search_radius = 150
        self.energy_consumption_rate = 0.05
        
    def update(self, birds: List[Bird]):
        """Update UAV position and behavior"""
        # Consume energy
        self.energy = max(0, self.energy - self.energy_consumption_rate)
        
        # Find target if none or target is too far
        if not self.target_bird or self._distance_to_bird(self.target_bird) > self.search_radius:
            self._find_new_target(birds)
            
        # Move towards target
        if self.target_bird:
            self._move_towards_target()
        else:
            # Patrol behavior when no target
            self._patrol_behavior()
            
        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
    def _find_new_target(self, birds: List[Bird]):
        """Find the best target bird based on simplified criteria"""
        best_target = None
        best_score = float('inf')
        
        for bird in birds:
            if bird.state != 'PERCHED':  # Don't target perched birds
                distance = self._distance_to_bird(bird)
                if distance <= self.search_radius:
                    # Simple scoring: prefer closer birds with lower energy
                    score = distance + (100 - bird.energy) * 0.5
                    if score < best_score:
                        best_score = score
                        best_target = bird
                        
        self.target_bird = best_target
        
    def _distance_to_bird(self, bird: Bird) -> float:
        """Calculate distance to a bird"""
        return math.sqrt((self.position[0] - bird.position[0])**2 + 
                        (self.position[1] - bird.position[1])**2)
                        
    def _move_towards_target(self):
        """Move UAV towards the target bird"""
        if not self.target_bird:
            return
            
        # Calculate direction to target
        dx = self.target_bird.position[0] - self.position[0]
        dy = self.target_bird.position[1] - self.position[1]
        
        # Normalize direction
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx /= distance
            dy /= distance
            
        # Apply movement with speed limit
        speed = min(self.max_speed, self.max_speed * (self.energy / 100.0))
        self.velocity[0] = dx * speed
        self.velocity[1] = dy * speed
        
    def _patrol_behavior(self):
        """Patrol behavior when no target is found"""
        # Simple circular patrol pattern
        center_x, center_y = 400, 300  # Center of screen
        radius = 100
        
        # Calculate desired position on patrol circle
        angle = (self.position[0] + self.position[1]) * 0.01  # Simple angle calculation
        desired_x = center_x + radius * math.cos(angle)
        desired_y = center_y + radius * math.sin(angle)
        
        # Move towards desired position
        dx = desired_x - self.position[0]
        dy = desired_y - self.position[1]
        
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx /= distance
            dy /= distance
            
        speed = self.max_speed * 0.5  # Slower patrol speed
        self.velocity[0] = dx * speed
        self.velocity[1] = dy * speed
        
    def get_status(self) -> dict:
        """Get UAV status information"""
        return {
            'position': self.position.copy(),
            'energy': self.energy,
            'target_bird': self.target_bird is not None,
            'search_radius': self.search_radius
        } 