"""
Bird Behavior Simulation for UAV Path Planning Demo
Simplified bird behavior simulation for demonstration purposes
"""

import random
import math
from typing import List, Tuple

class Bird:
    """Simplified bird behavior simulation for demo purposes"""
    
    STATES = ['CRUISING', 'SOARING', 'GLIDING', 'PERCHED', 'TAKING_OFF']
    
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float]):
        # Position and movement
        self.position = list(position)
        self.velocity = list(velocity)
        self.acceleration = [0, 0]
        self.altitude = random.randint(50, 200)
        self.heading = math.atan2(velocity[1], velocity[0])
        
        # Physical characteristics
        self.wingspan = random.uniform(1.0, 1.5)
        self.mass = random.uniform(0.3, 0.5)
        self.max_speed = random.uniform(10, 15)
        self.min_speed = 5
        self.max_force = 0.8
        self.glide_ratio = random.uniform(12, 15)
        
        # Energy and stamina
        self.energy = 100.0
        self.energy_consumption_rate = 0.1
        self.soaring_energy_gain = 0.2
        self.rest_energy_gain = 0.3
        
        # Behavioral state
        self.state = 'CRUISING'
        self.state_duration = 0
        self.perch_timer = 0
        self.in_formation = False
        
        # Environmental awareness
        self.thermal_locations = []
        self.perch_locations = [(100, 100), (700, 500), (300, 700)]
        self.wind = [0, 0]
        
    def update(self, birds: List['Bird'], bounds: Tuple[int, int], wind: Tuple[float, float]):
        """Update bird position and state based on simplified behavior"""
        self.wind = list(wind)
        self.state_duration += 1
        
        # Update energy levels
        self._update_energy()
        
        # State transitions
        self._update_state(birds, bounds)
        
        # Apply state-specific behavior
        if self.state == 'PERCHED':
            self._handle_perched_state()
        elif self.state == 'SOARING':
            self._handle_soaring_state()
        elif self.state == 'GLIDING':
            self._handle_gliding_state()
        elif self.state == 'TAKING_OFF':
            self._handle_takeoff_state()
        else:  # CRUISING
            self._handle_cruising_state(birds, bounds)
            
        # Apply wind effects
        self._apply_wind_effects()
        
        # Update position if not perched
        if self.state != 'PERCHED':
            self._update_position(bounds)
            
    def _update_energy(self):
        """Update bird's energy levels based on current state"""
        if self.state == 'PERCHED':
            self.energy = min(100, self.energy + self.rest_energy_gain)
        elif self.state == 'SOARING':
            self.energy = min(100, self.energy + self.soaring_energy_gain)
        elif self.state == 'GLIDING':
            self.energy = max(0, self.energy - self.energy_consumption_rate * 0.3)
        else:  # CRUISING or TAKING_OFF
            self.energy = max(0, self.energy - self.energy_consumption_rate)
            
    def _update_state(self, birds: List['Bird'], bounds: Tuple[int, int]):
        """Update bird's behavioral state"""
        if self.state == 'PERCHED':
            if self.perch_timer <= 0 and self.energy > 70:
                self.state = 'TAKING_OFF'
                self.state_duration = 0
        elif self.state == 'TAKING_OFF':
            if self.state_duration > 30:
                self.state = 'CRUISING'
                self.state_duration = 0
        else:
            # Check for perching conditions
            if self.energy < 30 and self._near_perch_location():
                self.state = 'PERCHED'
                self.perch_timer = random.randint(100, 200)
                self.velocity = [0, 0]
            # Check for thermal soaring conditions
            elif self._near_thermal() and random.random() < 0.1:
                self.state = 'SOARING'
            # Check for gliding conditions
            elif self.altitude > 100 and random.random() < 0.05:
                self.state = 'GLIDING'
            # Return to cruising if soaring/gliding too long
            elif (self.state in ['SOARING', 'GLIDING'] and 
                  self.state_duration > random.randint(100, 200)):
                self.state = 'CRUISING'
                
    def _handle_perched_state(self):
        """Handle behavior while perched"""
        self.perch_timer -= 1
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.altitude = 0
        
    def _handle_soaring_state(self):
        """Handle thermal soaring behavior"""
        # Spiral upward in thermal
        self.altitude = min(500, self.altitude + 2)
        angle = self.state_duration * 0.1
        speed = 3
        self.velocity = [
            speed * math.cos(angle),
            speed * math.sin(angle)
        ]
        
    def _handle_gliding_state(self):
        """Handle gliding behavior"""
        # Gradual descent based on glide ratio
        self.altitude = max(50, self.altitude - (self.min_speed / self.glide_ratio))
        # Maintain forward momentum
        speed = max(self.min_speed, 
                   math.sqrt(self.velocity[0]**2 + self.velocity[1]**2) * 0.99)
        self.velocity = [
            speed * math.cos(self.heading),
            speed * math.sin(self.heading)
        ]
        
    def _handle_takeoff_state(self):
        """Handle takeoff behavior"""
        # Gradual increase in speed and altitude
        self.altitude = min(100, self.altitude + 3)
        takeoff_speed = self.max_speed * (self.state_duration / 30)
        self.velocity = [
            takeoff_speed * math.cos(self.heading),
            takeoff_speed * math.sin(self.heading)
        ]
        
    def _handle_cruising_state(self, birds: List['Bird'], bounds: Tuple[int, int]):
        """Handle normal cruising flight with simplified flocking"""
        # Basic flocking behavior
        separation = self._separate(birds)
        alignment = self._align(birds)
        cohesion = self._cohere(birds)
        bounds_force = self._keep_within_bounds(bounds)
        
        # Weight forces based on energy levels
        energy_factor = self.energy / 100.0
        separation = [f * 2.0 for f in separation]
        alignment = [f * energy_factor for f in alignment]
        cohesion = [f * energy_factor for f in cohesion]
        bounds_force = [f * 1.5 for f in bounds_force]
        
        # Apply forces
        self.acceleration[0] += (separation[0] + alignment[0] + 
                               cohesion[0] + bounds_force[0])
        self.acceleration[1] += (separation[1] + alignment[1] + 
                               cohesion[1] + bounds_force[1])
                               
        # Update velocity with energy constraints
        self._update_velocity()
        
    def _update_velocity(self):
        """Update velocity based on acceleration and constraints"""
        # Apply acceleration
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        
        # Limit velocity based on energy and state
        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        max_speed = self.max_speed * (self.energy / 100.0)
        
        if speed > max_speed:
            self.velocity[0] = (self.velocity[0] / speed) * max_speed
            self.velocity[1] = (self.velocity[1] / speed) * max_speed
            
        # Reset acceleration
        self.acceleration = [0, 0]
        
    def _apply_wind_effects(self):
        """Apply wind effects to bird movement"""
        self.velocity[0] += self.wind[0] * 0.1
        self.velocity[1] += self.wind[1] * 0.1
        
    def _update_position(self, bounds: Tuple[int, int]):
        """Update bird position"""
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Keep within bounds
        self.position[0] = max(0, min(bounds[0], self.position[0]))
        self.position[1] = max(0, min(bounds[1], self.position[1]))
        
    def _near_thermal(self) -> bool:
        """Check if bird is near a thermal updraft"""
        for thermal in self.thermal_locations:
            distance = math.sqrt((self.position[0] - thermal[0])**2 + 
                               (self.position[1] - thermal[1])**2)
            if distance < 50:
                return True
        return False
        
    def _near_perch_location(self) -> bool:
        """Check if bird is near a perch location"""
        for perch in self.perch_locations:
            distance = math.sqrt((self.position[0] - perch[0])**2 + 
                               (self.position[1] - perch[1])**2)
            if distance < 30:
                return True
        return False
        
    def get_color(self) -> Tuple[int, int, int]:
        """Get bird color based on energy level"""
        if self.energy > 80:
            return (0, 255, 0)  # Green - high energy
        elif self.energy > 50:
            return (255, 255, 0)  # Yellow - medium energy
        elif self.energy > 20:
            return (255, 128, 0)  # Orange - low energy
        else:
            return (255, 0, 0)  # Red - very low energy
            
    def _separate(self, birds: List['Bird'], desired_separation: float = 25) -> List[float]:
        """Calculate separation force from other birds"""
        force = [0, 0]
        count = 0
        
        for bird in birds:
            if bird != self:
                distance = math.sqrt((self.position[0] - bird.position[0])**2 + 
                                   (self.position[1] - bird.position[1])**2)
                if distance < desired_separation and distance > 0:
                    # Calculate separation force
                    force[0] += (self.position[0] - bird.position[0]) / distance
                    force[1] += (self.position[1] - bird.position[1]) / distance
                    count += 1
                    
        if count > 0:
            force[0] /= count
            force[1] /= count
            
        return force
        
    def _align(self, birds: List['Bird'], neighbor_dist: float = 50) -> List[float]:
        """Calculate alignment force with nearby birds"""
        force = [0, 0]
        count = 0
        
        for bird in birds:
            if bird != self:
                distance = math.sqrt((self.position[0] - bird.position[0])**2 + 
                                   (self.position[1] - bird.position[1])**2)
                if distance < neighbor_dist:
                    force[0] += bird.velocity[0]
                    force[1] += bird.velocity[1]
                    count += 1
                    
        if count > 0:
            force[0] /= count
            force[1] /= count
            
        return force
        
    def _cohere(self, birds: List['Bird'], neighbor_dist: float = 50) -> List[float]:
        """Calculate cohesion force towards center of nearby birds"""
        center = [0, 0]
        count = 0
        
        for bird in birds:
            if bird != self:
                distance = math.sqrt((self.position[0] - bird.position[0])**2 + 
                                   (self.position[1] - bird.position[1])**2)
                if distance < neighbor_dist:
                    center[0] += bird.position[0]
                    center[1] += bird.position[1]
                    count += 1
                    
        if count > 0:
            center[0] /= count
            center[1] /= count
            return [(center[0] - self.position[0]) * 0.01, 
                   (center[1] - self.position[1]) * 0.01]
        return [0, 0]
        
    def _keep_within_bounds(self, bounds: Tuple[int, int]) -> List[float]:
        """Calculate force to keep bird within bounds"""
        force = [0, 0]
        margin = 50
        
        if self.position[0] < margin:
            force[0] = margin - self.position[0]
        elif self.position[0] > bounds[0] - margin:
            force[0] = (bounds[0] - margin) - self.position[0]
            
        if self.position[1] < margin:
            force[1] = margin - self.position[1]
        elif self.position[1] > bounds[1] - margin:
            force[1] = (bounds[1] - margin) - self.position[1]
            
        return [f * 0.1 for f in force] 