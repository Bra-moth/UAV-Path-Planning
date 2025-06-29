#!/usr/bin/env python3
"""
Learning UAV Video Generator
Creates a video showing UAV learning to chase bird swarms with adaptive behavior
"""

import cv2
import numpy as np
import time
import os
import sys
import math
import random
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from bird_simulation import Bird
from uav_controller import UAVController

class LearningUAVController(UAVController):
    """Enhanced UAV controller with learning capabilities"""
    
    def __init__(self, position):
        super().__init__(position)
        self.learning_rate = 0.01
        self.experience = []
        self.prediction_accuracy = 0.5
        self.adaptation_level = 0.0
        self.successful_captures = 0
        self.total_attempts = 0
        self.learning_phase = "EXPLORATION"  # EXPLORATION, LEARNING, OPTIMIZATION
        self.phase_timer = 0
        
    def update(self, birds):
        """Update UAV with learning behavior"""
        # Consume energy
        self.energy = max(0, self.energy - self.energy_consumption_rate)
        
        # Update learning phase
        self._update_learning_phase()
        
        # Find target with learning-based selection
        if not self.target_bird or self._distance_to_bird(self.target_bird) > self.search_radius:
            self._find_optimal_target(birds)
            
        # Move towards target with adaptive behavior
        if self.target_bird:
            self._adaptive_movement()
        else:
            self._patrol_behavior()
            
        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Learn from experience
        self._learn_from_experience()
        
    def _update_learning_phase(self):
        """Update the learning phase based on performance"""
        self.phase_timer += 1
        
        if self.phase_timer < 300:  # First 10 seconds
            self.learning_phase = "EXPLORATION"
        elif self.phase_timer < 600:  # Next 10 seconds
            self.learning_phase = "LEARNING"
        else:  # Final phase
            self.learning_phase = "OPTIMIZATION"
            
    def _find_optimal_target(self, birds):
        """Find optimal target using learned patterns"""
        best_target = None
        best_score = float('inf')
        
        for bird in birds:
            if bird.state != 'PERCHED':
                distance = self._distance_to_bird(bird)
                if distance <= self.search_radius:
                    # Enhanced scoring with learning
                    base_score = distance + (100 - bird.energy) * 0.5
                    
                    # Learning-based adjustments
                    if self.learning_phase == "EXPLORATION":
                        # Random exploration
                        score = base_score + random.uniform(-50, 50)
                    elif self.learning_phase == "LEARNING":
                        # Start using learned patterns
                        learned_bonus = self.adaptation_level * 20
                        score = base_score - learned_bonus
                    else:  # OPTIMIZATION
                        # Fully optimized selection
                        learned_bonus = self.adaptation_level * 50
                        prediction_bonus = self.prediction_accuracy * 30
                        score = base_score - learned_bonus - prediction_bonus
                    
                    if score < best_score:
                        best_score = score
                        best_target = bird
                        
        self.target_bird = best_target
        
    def _adaptive_movement(self):
        """Adaptive movement based on learning phase"""
        if not self.target_bird:
            return
            
        # Calculate base direction
        dx = self.target_bird.position[0] - self.position[0]
        dy = self.target_bird.position[1] - self.position[1]
        
        # Normalize direction
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx /= distance
            dy /= distance
            
        # Apply learning-based adjustments
        if self.learning_phase == "EXPLORATION":
            # Add exploration noise
            dx += random.uniform(-0.3, 0.3)
            dy += random.uniform(-0.3, 0.3)
        elif self.learning_phase == "LEARNING":
            # Start predicting movement
            predicted_x = self.target_bird.position[0] + self.target_bird.velocity[0] * 5
            predicted_y = self.target_bird.position[1] + self.target_bird.velocity[1] * 5
            pred_dx = predicted_x - self.position[0]
            pred_dy = predicted_y - self.position[1]
            pred_dist = math.sqrt(pred_dx**2 + pred_dy**2)
            if pred_dist > 0:
                pred_dx /= pred_dist
                pred_dy /= pred_dist
                # Blend current and predicted
                blend = self.adaptation_level
                dx = dx * (1 - blend) + pred_dx * blend
                dy = dy * (1 - blend) + pred_dy * blend
        else:  # OPTIMIZATION
            # Fully optimized movement with prediction
            predicted_x = self.target_bird.position[0] + self.target_bird.velocity[0] * 8
            predicted_y = self.target_bird.position[1] + self.target_bird.velocity[1] * 8
            pred_dx = predicted_x - self.position[0]
            pred_dy = predicted_y - self.position[1]
            pred_dist = math.sqrt(pred_dx**2 + pred_dy**2)
            if pred_dist > 0:
                pred_dx /= pred_dist
                pred_dy /= pred_dist
                # Use prediction with high confidence
                dx = pred_dx * 0.8 + dx * 0.2
                dy = pred_dy * 0.8 + dy * 0.2
            
        # Apply speed with learning-based optimization
        base_speed = min(self.max_speed, self.max_speed * (self.energy / 100.0))
        if self.learning_phase == "OPTIMIZATION":
            speed = base_speed * (1.0 + self.adaptation_level * 0.3)
        else:
            speed = base_speed
            
        self.velocity[0] = dx * speed
        self.velocity[1] = dy * speed
        
    def _learn_from_experience(self):
        """Learn from current experience"""
        if self.target_bird:
            # Calculate success metrics
            distance = self._distance_to_bird(self.target_bird)
            
            # Update adaptation level based on performance
            if distance < 30:  # Close to target
                self.adaptation_level = min(1.0, self.adaptation_level + self.learning_rate)
                if distance < 15:  # Very close - successful capture
                    self.successful_captures += 1
            else:
                # Gradually decrease adaptation if not successful
                self.adaptation_level = max(0.0, self.adaptation_level - self.learning_rate * 0.1)
                
            # Update prediction accuracy
            if self.learning_phase in ["LEARNING", "OPTIMIZATION"]:
                # Simulate prediction accuracy improvement
                self.prediction_accuracy = min(1.0, self.prediction_accuracy + self.learning_rate * 0.5)
                
            self.total_attempts += 1

class EnhancedBirdSwarm:
    """Enhanced bird swarm with more complex flocking behavior"""
    
    def __init__(self, num_birds=15, bounds=(1920, 1080)):
        self.birds = []
        self.bounds = bounds
        self.swarm_center = [bounds[0]//2, bounds[1]//2]
        self.swarm_velocity = [0, 0]
        
        # Initialize birds in a more natural formation
        for i in range(num_birds):
            angle = (i / num_birds) * 2 * math.pi
            radius = random.uniform(50, 150)
            x = self.swarm_center[0] + radius * math.cos(angle)
            y = self.swarm_center[1] + radius * math.sin(angle)
            vel = (random.uniform(-2, 2), random.uniform(-2, 2))
            self.birds.append(Bird((x, y), vel))
            
    def update(self, wind=(0, 0)):
        """Update all birds with enhanced flocking"""
        # Update swarm center and velocity
        if len(self.birds) > 0:
            center_x = sum(b.position[0] for b in self.birds) / len(self.birds)
            center_y = sum(b.position[1] for b in self.birds) / len(self.birds)
            self.swarm_center = [center_x, center_y]
            
            # Add some swarm-level movement
            self.swarm_velocity[0] += random.uniform(-0.1, 0.1)
            self.swarm_velocity[1] += random.uniform(-0.1, 0.1)
            
            # Limit swarm velocity
            swarm_speed = math.sqrt(self.swarm_velocity[0]**2 + self.swarm_velocity[1]**2)
            if swarm_speed > 2:
                self.swarm_velocity[0] = (self.swarm_velocity[0] / swarm_speed) * 2
                self.swarm_velocity[1] = (self.swarm_velocity[1] / swarm_speed) * 2
        
        # Update individual birds
        bounds = self.bounds
        for bird in self.birds:
            bird.update(self.birds, bounds, wind)
            
            # Add swarm influence
            bird.velocity[0] += self.swarm_velocity[0] * 0.1
            bird.velocity[1] += self.swarm_velocity[1] * 0.1

class LearningVideoGenerator:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.fps = 30
        self.output_filename = f"uav_learning_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(self.output_filename, fourcc, self.fps, (width, height))
        
        # Initialize components
        self.bird_swarm = EnhancedBirdSwarm(20, (width, height))
        self.uav = LearningUAVController((width//2, height//2))
        self.frame_count = 0
        self.animation_frame = 0
        
    def create_title_screen(self):
        """Create title screen for learning demo"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Animated background
        for y in range(self.height):
            for x in range(self.width):
                time_factor = self.animation_frame * 0.02
                r = int(30 + 20 * np.sin(x * 0.01 + time_factor))
                g = int(50 + 30 * np.sin(y * 0.01 + time_factor))
                b = int(80 + 40 * np.sin((x + y) * 0.005 + time_factor))
                frame[y, x] = [r, g, b]
        
        # Title
        title = "UAV Learning to Chase Bird Swarms"
        subtitle = "Adaptive Path Planning & Target Acquisition"
        
        font_large = cv2.FONT_HERSHEY_DUPLEX
        font_small = cv2.FONT_HERSHEY_SIMPLEX
        
        # Title with glow
        title_size = cv2.getTextSize(title, font_large, 2.5, 5)[0]
        title_x = (self.width - title_size[0]) // 2
        title_y = self.height // 2 - 80
        
        for i in range(5, 0, -1):
            alpha = 0.3 - i * 0.05
            color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
            cv2.putText(frame, title, (title_x, title_y), font_large, 2.5, color, i)
        
        cv2.putText(frame, title, (title_x, title_y), font_large, 2.5, (255, 255, 255), 5)
        
        # Subtitle
        subtitle_size = cv2.getTextSize(subtitle, font_small, 1.2, 3)[0]
        subtitle_x = (self.width - subtitle_size[0]) // 2
        subtitle_y = self.height // 2 + 20
        
        color_val = int(200 + 55 * np.sin(self.animation_frame * 0.1))
        cv2.putText(frame, subtitle, (subtitle_x, subtitle_y), font_small, 1.2, (color_val, color_val, color_val), 3)
        
        # Learning phases indicator
        phases = ["EXPLORATION", "LEARNING", "OPTIMIZATION"]
        phase_x = 50
        phase_y = self.height - 100
        
        for i, phase in enumerate(phases):
            x = phase_x + i * 300
            color = (100, 100, 100) if i == 0 else (150, 150, 150)
            cv2.putText(frame, phase, (x, phase_y), font_small, 0.8, color, 2)
        
        return frame
    
    def create_learning_simulation_frame(self):
        """Create simulation frame showing learning process"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create gradient background
        for y in range(self.height):
            color = int(20 + (y / self.height) * 60)
            frame[y, :] = [color//3, color//2, color]
        
        # Add subtle grid
        for x in range(0, self.width, 100):
            cv2.line(frame, (x, 0), (x, self.height), (30, 30, 30), 1)
        for y in range(0, self.height, 100):
            cv2.line(frame, (0, y), (self.width, y), (30, 30, 30), 1)
        
        # Update bird swarm
        self.bird_swarm.update()
        
        # Draw birds with enhanced visuals
        for bird in self.bird_swarm.birds:
            x, y = int(bird.position[0]), int(bird.position[1])
            
            # Shadow
            cv2.circle(frame, (x+3, y+3), 12, (15, 15, 15), -1)
            
            # Bird body
            color = bird.get_color()
            cv2.circle(frame, (x, y), 12, color, -1)
            cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)
            
            # Direction indicator
            direction_x = int(x + bird.velocity[0] * 8)
            direction_y = int(y + bird.velocity[1] * 8)
            cv2.line(frame, (x, y), (direction_x, direction_y), (255, 255, 255), 2)
            
            # State indicator
            state_colors = {
                'CRUISING': (0, 255, 0),
                'SOARING': (255, 255, 0),
                'GLIDING': (0, 255, 255),
                'PERCHED': (128, 128, 128),
                'TAKING_OFF': (255, 128, 0)
            }
            state_color = state_colors.get(bird.state, (255, 255, 255))
            cv2.circle(frame, (x+18, y-18), 6, state_color, -1)
        
        # Update and draw UAV
        self.uav.update(self.bird_swarm.birds)
        uav_x, uav_y = int(self.uav.position[0]), int(self.uav.position[1])
        
        # UAV shadow
        cv2.circle(frame, (uav_x+4, uav_y+4), 18, (15, 15, 15), -1)
        
        # UAV body with learning phase color
        phase_colors = {
            "EXPLORATION": (255, 128, 0),  # Orange
            "LEARNING": (255, 255, 0),     # Yellow
            "OPTIMIZATION": (0, 255, 0)    # Green
        }
        uav_color = phase_colors.get(self.uav.learning_phase, (255, 0, 0))
        cv2.circle(frame, (uav_x, uav_y), 18, uav_color, -1)
        cv2.circle(frame, (uav_x, uav_y), 18, (255, 255, 255), 3)
        
        # UAV direction
        direction_x = int(uav_x + self.uav.velocity[0] * 10)
        direction_y = int(uav_y + self.uav.velocity[1] * 10)
        cv2.line(frame, (uav_x, uav_y), (direction_x, direction_y), (255, 255, 255), 4)
        
        # Target line and prediction
        if self.uav.target_bird:
            target_x, target_y = int(self.uav.target_bird.position[0]), int(self.uav.target_bird.position[1])
            
            # Current target line
            cv2.line(frame, (uav_x, uav_y), (target_x, target_y), (255, 255, 0), 3)
            
            # Prediction line (in learning phases)
            if self.uav.learning_phase in ["LEARNING", "OPTIMIZATION"]:
                pred_x = int(target_x + self.uav.target_bird.velocity[0] * 10)
                pred_y = int(target_y + self.uav.target_bird.velocity[1] * 10)
                cv2.line(frame, (target_x, target_y), (pred_x, pred_y), (0, 255, 255), 2)
                cv2.circle(frame, (pred_x, pred_y), 8, (0, 255, 255), 2)
            
            # Target indicator
            cv2.circle(frame, (target_x, target_y), 18, (255, 255, 0), 2)
        
        # Enhanced UI with learning metrics
        # Main panel
        cv2.rectangle(frame, (10, 10), (450, 220), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (450, 220), (255, 255, 255), 2)
        
        # Title
        cv2.putText(frame, "UAV Learning Simulation", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        
        # Learning metrics
        cv2.putText(frame, f"Phase: {self.uav.learning_phase}", (20, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Adaptation: {self.uav.adaptation_level:.2f}", (20, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Prediction: {self.uav.prediction_accuracy:.2f}", (20, 130), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Success Rate: {self.uav.successful_captures}/{self.uav.total_attempts}", (20, 160), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Energy: {self.uav.energy:.1f}%", (20, 190), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Phase progress indicator
        phase_x = 20
        phase_y = 250
        cv2.putText(frame, "Learning Progress:", (phase_x, phase_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Progress bar
        bar_width = 400
        bar_height = 20
        bar_x = phase_x
        bar_y = phase_y + 20
        
        # Background bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
        
        # Progress based on learning phase
        if self.uav.learning_phase == "EXPLORATION":
            progress = min(1.0, self.uav.phase_timer / 300)
        elif self.uav.learning_phase == "LEARNING":
            progress = 0.33 + min(0.33, (self.uav.phase_timer - 300) / 300)
        else:
            progress = 0.66 + min(0.34, (self.uav.phase_timer - 600) / 300)
        
        progress_width = int(bar_width * progress)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), (0, 255, 0), -1)
        
        # Phase labels
        phase_labels = ["Exploration", "Learning", "Optimization"]
        for i, label in enumerate(phase_labels):
            x = bar_x + i * (bar_width // 3)
            color = (255, 255, 255) if i * 0.33 <= progress else (100, 100, 100)
            cv2.putText(frame, label, (x, bar_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Enhanced legend
        legend_x = self.width - 280
        legend_y = 50
        
        cv2.rectangle(frame, (legend_x-10, legend_y-10), (legend_x+270, legend_y+160), (0, 0, 0), -1)
        cv2.rectangle(frame, (legend_x-10, legend_y-10), (legend_x+270, legend_y+160), (255, 255, 255), 2)
        
        cv2.putText(frame, "Legend:", (legend_x, legend_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        legend_items = [
            ((255, 128, 0), "UAV (Exploration)"),
            ((255, 255, 0), "UAV (Learning)"),
            ((0, 255, 0), "UAV (Optimization)"),
            ((0, 255, 0), "Birds (High Energy)"),
            ((255, 255, 0), "Birds (Medium Energy)"),
            ((255, 128, 0), "Birds (Low Energy)"),
            ((255, 255, 0), "Target Line"),
            ((0, 255, 255), "Prediction")
        ]
        
        for i, (color, label) in enumerate(legend_items):
            y_pos = legend_y + 25 + i * 18
            cv2.circle(frame, (legend_x, y_pos), 6, color, -1)
            cv2.putText(frame, label, (legend_x + 15, y_pos + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def create_conclusion_screen(self):
        """Create conclusion screen showing learning results"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Animated background
        for y in range(self.height):
            for x in range(self.width):
                time_factor = self.animation_frame * 0.01
                r = int(20 + 10 * np.sin(x * 0.01 + time_factor))
                g = int(30 + 15 * np.sin(y * 0.01 + time_factor))
                b = int(40 + 20 * np.sin((x + y) * 0.005 + time_factor))
                frame[y, x] = [r, g, b]
        
        # Title
        cv2.putText(frame, "Learning Complete", (50, 100), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 255), 4)
        
        # Results
        success_rate = self.uav.successful_captures / max(1, self.uav.total_attempts) * 100
        
        content = [
            "Learning Results:",
            "",
            f"• Final Adaptation Level: {self.uav.adaptation_level:.2f}",
            f"• Prediction Accuracy: {self.uav.prediction_accuracy:.2f}",
            f"• Success Rate: {success_rate:.1f}%",
            f"• Total Attempts: {self.uav.total_attempts}",
            f"• Successful Captures: {self.uav.successful_captures}",
            "",
            "Learning Phases Completed:",
            "",
            "• Exploration Phase: Random target selection",
            "• Learning Phase: Pattern recognition",
            "• Optimization Phase: Predictive targeting",
            "",
            "The UAV has learned to:",
            "",
            "• Predict bird movement patterns",
            "• Optimize path planning",
            "• Adapt to swarm behavior",
            "• Improve capture success rate",
            "",
            "For more information about the full research project:",
            "",
            "Author: Solomon Makuwa",
            "Email: 202211185@spu.ac.za",
            "Institution: Sol Plaatje University",
            "Supervisors: Lebelo Serutla, Dr Alfred Mwanza"
        ]
        
        y_start = 200
        for i, line in enumerate(content):
            y = y_start + i * 35
            
            # Animated text appearance
            if self.animation_frame > i * 8:
                if line.startswith("•"):
                    color = (0, 255, 255)
                elif "Author:" in line or "Email:" in line or "Institution:" in line or "Supervisors:" in line:
                    color = (255, 255, 0)
                elif "Learning Results:" in line or "Learning Phases Completed:" in line or "The UAV has learned to:" in line:
                    color = (255, 255, 255)
                else:
                    color = (200, 200, 200)
                
                cv2.putText(frame, line, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return frame
    
    def generate_learning_video(self):
        """Generate the complete learning demo video"""
        print("Generating UAV Learning Demo Video...")
        print(f"Output file: {self.output_filename}")
        
        # Section durations
        intro_duration = 4 * self.fps  # 4 seconds
        simulation_duration = 30 * self.fps  # 30 seconds
        conclusion_duration = 6 * self.fps  # 6 seconds
        
        total_frames = intro_duration + simulation_duration + conclusion_duration
        
        # Generate video frames
        for frame_num in range(total_frames):
            if frame_num < intro_duration:
                # Intro section
                frame = self.create_title_screen()
            elif frame_num < intro_duration + simulation_duration:
                # Learning simulation section
                frame = self.create_learning_simulation_frame()
                self.frame_count += 1
            else:
                # Conclusion section
                frame = self.create_conclusion_screen()
            
            # Update animation frame
            self.animation_frame += 1
            
            # Write frame
            self.video_writer.write(frame)
            
            # Progress indicator
            if frame_num % 30 == 0:
                progress = (frame_num / total_frames) * 100
                print(f"Progress: {progress:.1f}%")
        
        # Release video writer
        self.video_writer.release()
        
        print(f"Learning video generation complete: {self.output_filename}")
        print(f"Video duration: {total_frames / self.fps:.1f} seconds")
        
        return self.output_filename

def main():
    """Main function to generate the learning demo video"""
    print("UAV Learning Demo Video Generator")
    print("=" * 50)
    
    # Create learning video generator
    generator = LearningVideoGenerator()
    
    # Generate video
    output_file = generator.generate_learning_video()
    
    print("\nLearning video generation completed successfully!")
    print(f"Output file: {output_file}")
    print("\nThis video showcases:")
    print("- UAV learning to chase bird swarms")
    print("- Adaptive path planning")
    print("- Three learning phases")
    print("- Real-time adaptation")
    print("- Success rate improvement")
    print("\nYou can now share this video to showcase your UAV learning capabilities.")

if __name__ == "__main__":
    main() 