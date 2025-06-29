#!/usr/bin/env python3
"""
Enhanced Demo Video Generator for UAV Path Planning
Creates a comprehensive video showcasing detailed drone specifications and UAV simulation
"""

import cv2
import numpy as np
import time
import os
import sys
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from bird_simulation import Bird
from uav_controller import UAVController

class EnhancedVideoGenerator:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.fps = 30
        self.output_filename = f"uav_enhanced_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(self.output_filename, fourcc, self.fps, (width, height))
        
        # Initialize simulation components
        self.birds = []
        self.uav = UAVController((width//2, height//2))
        self.frame_count = 0
        self.animation_frame = 0
        
    def create_animated_title(self, title, subtitle=""):
        """Create an animated title screen"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create animated gradient background
        for y in range(self.height):
            for x in range(self.width):
                # Animated gradient
                time_factor = self.animation_frame * 0.02
                r = int(50 + 30 * np.sin(x * 0.01 + time_factor))
                g = int(50 + 30 * np.sin(y * 0.01 + time_factor))
                b = int(100 + 50 * np.sin((x + y) * 0.005 + time_factor))
                frame[y, x] = [r, g, b]
        
        # Add animated title
        font_large = cv2.FONT_HERSHEY_DUPLEX
        font_small = cv2.FONT_HERSHEY_SIMPLEX
        
        # Title with glow effect
        title_size = cv2.getTextSize(title, font_large, 3, 5)[0]
        title_x = (self.width - title_size[0]) // 2
        title_y = self.height // 2 - 100
        
        # Glow effect
        for i in range(5, 0, -1):
            alpha = 0.3 - i * 0.05
            color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
            cv2.putText(frame, title, (title_x, title_y), font_large, 3, color, i)
        
        # Main title
        cv2.putText(frame, title, (title_x, title_y), font_large, 3, (255, 255, 255), 5)
        
        # Animated subtitle
        if subtitle:
            subtitle_size = cv2.getTextSize(subtitle, font_small, 1.5, 3)[0]
            subtitle_x = (self.width - subtitle_size[0]) // 2
            subtitle_y = self.height // 2 + 50
            
            # Animated color
            color_val = int(200 + 55 * np.sin(self.animation_frame * 0.1))
            cv2.putText(frame, subtitle, (subtitle_x, subtitle_y), font_small, 1.5, (color_val, color_val, color_val), 3)
        
        # Add animated drone icon
        self.draw_animated_drone(frame, (self.width - 200, 200))
        
        return frame
    
    def draw_animated_drone(self, frame, position):
        """Draw an animated drone icon"""
        x, y = position
        time_factor = self.animation_frame * 0.1
        
        # Rotating propellers
        for i in range(4):
            angle = time_factor + i * np.pi / 2
            prop_x = x + int(60 * np.cos(angle))
            prop_y = y + int(60 * np.sin(angle))
            cv2.circle(frame, (prop_x, prop_y), 8, (100, 100, 100), -1)
            cv2.circle(frame, (prop_x, prop_y), 8, (255, 255, 255), 2)
        
        # Main body
        cv2.rectangle(frame, (x-50, y-30), (x+50, y+30), (80, 80, 80), -1)
        cv2.rectangle(frame, (x-50, y-30), (x+50, y+30), (255, 255, 255), 3)
        
        # Camera with pulsing effect
        pulse = int(20 + 10 * np.sin(self.animation_frame * 0.2))
        cv2.circle(frame, (x, y), pulse, (0, 0, 255), -1)
        cv2.circle(frame, (x, y), pulse, (255, 255, 255), 2)
    
    def create_detailed_specifications_screen(self):
        """Create detailed drone specifications screen"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background with subtle pattern
        frame.fill(20)
        for y in range(0, self.height, 20):
            cv2.line(frame, (0, y), (self.width, y), (25, 25, 25), 1)
        
        # Title with animation
        title = "UAV Technical Specifications"
        cv2.putText(frame, title, (50, 80), cv2.FONT_HERSHEY_DUPLEX, 2.5, (255, 255, 255), 3)
        
        # Detailed specifications with categories
        specs_data = {
            "Physical Characteristics": [
                ("Wingspan", "1.2 - 1.8 meters", "Adjustable for mission requirements"),
                ("Mass", "2.5 - 4.0 kg", "Including payload and fuel"),
                ("Length", "1.0 - 1.5 meters", "Compact design for portability"),
                ("Height", "0.3 - 0.5 meters", "Streamlined aerodynamic profile")
            ],
            "Performance Parameters": [
                ("Max Speed", "25 m/s (90 km/h)", "Cruise speed: 15-20 m/s"),
                ("Service Ceiling", "4000m", "Maximum operational altitude"),
                ("Endurance", "45-60 minutes", "Typical mission duration"),
                ("Range", "15-25 km", "Line-of-sight communication range"),
                ("Climb Rate", "5 m/s", "Vertical ascent capability"),
                ("Descent Rate", "3 m/s", "Controlled landing approach")
            ],
            "Payload & Capacity": [
                ("Payload Capacity", "1.5 kg", "Maximum additional weight"),
                ("Battery Capacity", "5000 mAh", "Lithium-polymer battery"),
                ("Fuel Capacity", "2.0 L", "For hybrid propulsion systems"),
                ("Sensor Payload", "0.8 kg", "Camera, GPS, IMU, etc.")
            ],
            "Sensor Systems": [
                ("HD Camera", "4K resolution", "30fps video recording"),
                ("GPS Module", "High-precision", "±2m accuracy"),
                ("IMU", "6-axis stabilization", "Gyroscope + Accelerometer"),
                ("Altimeter", "Barometric + GPS", "Dual redundancy"),
                ("Compass", "Digital magnetometer", "Heading reference"),
                ("Temperature", "Digital sensor", "Environmental monitoring")
            ],
            "Communication Systems": [
                ("Radio Control", "2.4 GHz", "Manual override capability"),
                ("Telemetry", "915 MHz", "Real-time data transmission"),
                ("Video Link", "5.8 GHz", "Live video streaming"),
                ("GPS Signal", "L1/L2 bands", "Dual-frequency positioning")
            ]
        }
        
        # Draw specifications
        y_start = 150
        x_left = 50
        x_right = self.width // 2 + 50
        
        for category, items in specs_data.items():
            # Category header
            cv2.putText(frame, category, (x_left, y_start), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            y_start += 40
            
            # Items
            for item in items:
                # Parameter name
                cv2.putText(frame, f"• {item[0]}:", (x_left + 20, y_start), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
                # Value
                cv2.putText(frame, item[1], (x_left + 200, y_start), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # Description
                cv2.putText(frame, f"  {item[2]}", (x_left + 20, y_start + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
                
                y_start += 50
            
            y_start += 20
            
            # Switch to right column if needed
            if y_start > self.height - 200:
                y_start = 190
                x_left = x_right
        
        # Add detailed drone diagram
        self.draw_detailed_drone_diagram(frame, (self.width - 400, 200))
        
        return frame
    
    def draw_detailed_drone_diagram(self, frame, position):
        """Draw a detailed drone diagram with labels"""
        x, y = position
        
        # Main body
        cv2.rectangle(frame, (x-60, y-40), (x+60, y+40), (100, 100, 100), -1)
        cv2.rectangle(frame, (x-60, y-40), (x+60, y+40), (255, 255, 255), 3)
        
        # Wings
        cv2.rectangle(frame, (x-120, y-10), (x+120, y+10), (80, 80, 80), -1)
        cv2.rectangle(frame, (x-120, y-10), (x+120, y+10), (200, 200, 200), 2)
        
        # Propellers
        prop_positions = [(x-80, y-60), (x+80, y-60), (x-80, y+60), (x+80, y+60)]
        for px, py in prop_positions:
            cv2.circle(frame, (px, py), 20, (60, 60, 60), -1)
            cv2.circle(frame, (px, py), 20, (255, 255, 255), 2)
        
        # Camera
        cv2.circle(frame, (x, y), 12, (0, 0, 255), -1)
        cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)
        
        # GPS antenna
        cv2.circle(frame, (x+40, y-30), 8, (0, 255, 0), -1)
        cv2.circle(frame, (x+40, y-30), 8, (255, 255, 255), 1)
        
        # Labels
        labels = [
            ("Camera", (x-30, y+60)),
            ("GPS", (x+30, y-50)),
            ("Propellers", (x-40, y-80)),
            ("Wings", (x-40, y+80)),
            ("Body", (x-30, y))
        ]
        
        for label, pos in labels:
            cv2.putText(frame, label, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def create_enhanced_simulation_frame(self):
        """Create an enhanced simulation frame with better visuals"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create gradient background
        for y in range(self.height):
            color = int(30 + (y / self.height) * 70)
            frame[y, :] = [color//3, color//2, color]
        
        # Add grid pattern
        for x in range(0, self.width, 50):
            cv2.line(frame, (x, 0), (x, self.height), (40, 40, 40), 1)
        for y in range(0, self.height, 50):
            cv2.line(frame, (0, y), (self.width, y), (40, 40, 40), 1)
        
        # Update birds
        wind = (0, 0)
        bounds = (self.width, self.height)
        
        # Initialize birds if needed
        if len(self.birds) == 0:
            for i in range(12):
                pos = (np.random.randint(100, self.width-100), np.random.randint(100, self.height-100))
                vel = (np.random.uniform(-2, 2), np.random.uniform(-2, 2))
                self.birds.append(Bird(pos, vel))
        
        # Update and draw birds with enhanced visuals
        for bird in self.birds:
            bird.update(self.birds, bounds, wind)
            
            # Draw bird with shadow
            x, y = int(bird.position[0]), int(bird.position[1])
            
            # Shadow
            cv2.circle(frame, (x+2, y+2), 10, (20, 20, 20), -1)
            
            # Bird body
            color = bird.get_color()
            cv2.circle(frame, (x, y), 10, color, -1)
            cv2.circle(frame, (x, y), 10, (255, 255, 255), 2)
            
            # Bird direction indicator
            direction_x = int(x + bird.velocity[0] * 5)
            direction_y = int(y + bird.velocity[1] * 5)
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
            cv2.circle(frame, (x+15, y-15), 5, state_color, -1)
        
        # Update and draw UAV with enhanced visuals
        self.uav.update(self.birds)
        uav_x, uav_y = int(self.uav.position[0]), int(self.uav.position[1])
        
        # UAV shadow
        cv2.circle(frame, (uav_x+3, uav_y+3), 15, (20, 20, 20), -1)
        
        # UAV body
        cv2.circle(frame, (uav_x, uav_y), 15, (255, 0, 0), -1)
        cv2.circle(frame, (uav_x, uav_y), 15, (255, 255, 255), 3)
        
        # UAV direction
        direction_x = int(uav_x + self.uav.velocity[0] * 8)
        direction_y = int(uav_y + self.uav.velocity[1] * 8)
        cv2.line(frame, (uav_x, uav_y), (direction_x, direction_y), (255, 255, 255), 3)
        
        # UAV target line if tracking
        if self.uav.target_bird:
            target_x, target_y = int(self.uav.target_bird.position[0]), int(self.uav.target_bird.position[1])
            cv2.line(frame, (uav_x, uav_y), (target_x, target_y), (255, 255, 0), 3)
            
            # Target indicator
            cv2.circle(frame, (target_x, target_y), 15, (255, 255, 0), 2)
        
        # Enhanced UI elements
        # Background panel
        cv2.rectangle(frame, (10, 10), (400, 180), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (400, 180), (255, 255, 255), 2)
        
        # Title
        cv2.putText(frame, "UAV Path Planning Simulation", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        
        # Metrics
        cv2.putText(frame, f"Birds Active: {len(self.birds)}", (20, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"UAV Energy: {self.uav.energy:.1f}%", (20, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Frame: {self.frame_count}", (20, 130), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Target: {'Yes' if self.uav.target_bird else 'No'}", (20, 160), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Enhanced legend
        legend_x = self.width - 250
        legend_y = 50
        
        # Legend background
        cv2.rectangle(frame, (legend_x-10, legend_y-10), (legend_x+240, legend_y+120), (0, 0, 0), -1)
        cv2.rectangle(frame, (legend_x-10, legend_y-10), (legend_x+240, legend_y+120), (255, 255, 255), 2)
        
        cv2.putText(frame, "Legend:", (legend_x, legend_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Legend items
        legend_items = [
            ((255, 0, 0), "UAV"),
            ((0, 255, 0), "Birds (High Energy)"),
            ((255, 255, 0), "Birds (Medium Energy)"),
            ((255, 128, 0), "Birds (Low Energy)"),
            ((255, 255, 0), "Target Line")
        ]
        
        for i, (color, label) in enumerate(legend_items):
            y_pos = legend_y + 25 + i * 20
            cv2.circle(frame, (legend_x, y_pos), 6, color, -1)
            cv2.putText(frame, label, (legend_x + 15, y_pos + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def create_conclusion_screen(self):
        """Create enhanced conclusion screen"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Animated background
        for y in range(self.height):
            for x in range(self.width):
                time_factor = self.animation_frame * 0.01
                r = int(20 + 10 * np.sin(x * 0.01 + time_factor))
                g = int(20 + 10 * np.sin(y * 0.01 + time_factor))
                b = int(30 + 15 * np.sin((x + y) * 0.005 + time_factor))
                frame[y, x] = [r, g, b]
        
        # Title
        cv2.putText(frame, "Demo Complete", (50, 100), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 255), 4)
        
        # Content with animations
        content = [
            "This demonstration showcases:",
            "",
            "• Real-time UAV path planning algorithms",
            "• Dynamic bird behavior simulation",
            "• 3D environment visualization",
            "• Energy-efficient navigation systems",
            "• Advanced target acquisition methods",
            "• Flocking behavior modeling",
            "• Thermal updraft utilization",
            "",
            "For more information about the full research project:",
            "",
            "Author: Solomon Makuwa",
            "Email: 202211185@spu.ac.za",
            "Institution: Sol Plaatje University",
            "Supervisors: Lebelo Serutla, Dr Alfred Mwanza",
            "",
            "Thank you for watching!"
        ]
        
        y_start = 200
        for i, line in enumerate(content):
            y = y_start + i * 40
            
            # Animated text appearance
            if self.animation_frame > i * 10:
                if line.startswith("•"):
                    color = (0, 255, 255)
                elif "Author:" in line or "Email:" in line or "Institution:" in line or "Supervisors:" in line:
                    color = (255, 255, 0)
                elif "Thank you" in line:
                    # Pulsing effect for thank you
                    pulse = int(200 + 55 * np.sin(self.animation_frame * 0.2))
                    color = (pulse, pulse, pulse)
                else:
                    color = (200, 200, 200)
                
                cv2.putText(frame, line, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        return frame
    
    def generate_enhanced_video(self):
        """Generate the complete enhanced demo video"""
        print("Generating Enhanced UAV Demo Video...")
        print(f"Output file: {self.output_filename}")
        
        # Section durations (in frames)
        intro_duration = 5 * self.fps  # 5 seconds
        specs_duration = 12 * self.fps  # 12 seconds
        simulation_duration = 20 * self.fps  # 20 seconds
        conclusion_duration = 6 * self.fps  # 6 seconds
        
        total_frames = intro_duration + specs_duration + simulation_duration + conclusion_duration
        
        # Generate video frames
        for frame_num in range(total_frames):
            if frame_num < intro_duration:
                # Intro section
                frame = self.create_animated_title(
                    "UAV Path Planning Demo",
                    "Advanced Drone Specifications & Simulation"
                )
            elif frame_num < intro_duration + specs_duration:
                # Specifications section
                frame = self.create_detailed_specifications_screen()
            elif frame_num < intro_duration + specs_duration + simulation_duration:
                # Simulation section
                frame = self.create_enhanced_simulation_frame()
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
        
        print(f"Enhanced video generation complete: {self.output_filename}")
        print(f"Video duration: {total_frames / self.fps:.1f} seconds")
        
        return self.output_filename

def main():
    """Main function to generate the enhanced demo video"""
    print("Enhanced UAV Path Planning Demo Video Generator")
    print("=" * 60)
    
    # Create enhanced video generator
    generator = EnhancedVideoGenerator()
    
    # Generate video
    output_file = generator.generate_enhanced_video()
    
    print("\nEnhanced video generation completed successfully!")
    print(f"Output file: {output_file}")
    print("\nThis video showcases:")
    print("- Detailed drone specifications")
    print("- Enhanced visual effects")
    print("- Comprehensive simulation")
    print("- Professional presentation")
    print("\nYou can now share this video to showcase your UAV path planning research.")

if __name__ == "__main__":
    main() 