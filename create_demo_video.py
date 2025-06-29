#!/usr/bin/env python3
"""
Demo Video Generator for UAV Path Planning
Creates a video showcasing drone specifications and UAV simulation
"""

import cv2
import numpy as np
import time
import os
from datetime import datetime
from bird_simulation import Bird
from uav_controller import UAVController

class VideoGenerator:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.fps = 30
        self.output_filename = f"uav_demo_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(self.output_filename, fourcc, self.fps, (width, height))
        
        # Initialize simulation components
        self.birds = []
        self.uav = UAVController((width//2, height//2))
        self.frame_count = 0
        self.section = 0  # 0: Intro, 1: Specs, 2: Simulation, 3: Conclusion
        self.section_timer = 0
        
    def create_title_screen(self, title, subtitle=""):
        """Create a title screen"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create gradient background
        for y in range(self.height):
            color = int(50 + (y / self.height) * 100)
            frame[y, :] = [color//3, color//2, color]
        
        # Add title
        font_large = cv2.FONT_HERSHEY_DUPLEX
        font_small = cv2.FONT_HERSHEY_SIMPLEX
        
        # Title
        title_size = cv2.getTextSize(title, font_large, 2, 3)[0]
        title_x = (self.width - title_size[0]) // 2
        title_y = self.height // 2 - 50
        cv2.putText(frame, title, (title_x, title_y), font_large, 2, (255, 255, 255), 3)
        
        # Subtitle
        if subtitle:
            subtitle_size = cv2.getTextSize(subtitle, font_small, 1, 2)[0]
            subtitle_x = (self.width - subtitle_size[0]) // 2
            subtitle_y = self.height // 2 + 50
            cv2.putText(frame, subtitle, (subtitle_x, subtitle_y), font_small, 1, (200, 200, 200), 2)
        
        return frame
    
    def create_specifications_screen(self):
        """Create drone specifications screen"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background
        frame.fill(30)
        
        # Title
        cv2.putText(frame, "UAV Specifications", (50, 80), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 2)
        
        # Specifications
        specs = [
            ("Physical Characteristics:", ""),
            ("• Wingspan: 1.2 - 1.8 meters", (100, 150)),
            ("• Mass: 2.5 - 4.0 kg", (100, 180)),
            ("• Max Speed: 25 m/s", (100, 210)),
            ("• Service Ceiling: 4000m", (100, 240)),
            ("", ""),
            ("Performance Parameters:", ""),
            ("• Endurance: 45-60 minutes", (100, 300)),
            ("• Range: 15-25 km", (100, 330)),
            ("• Payload Capacity: 1.5 kg", (100, 360)),
            ("• Climb Rate: 5 m/s", (100, 390)),
            ("", ""),
            ("Sensor Systems:", ""),
            ("• HD Camera: 4K resolution", (100, 450)),
            ("• GPS: High-precision navigation", (100, 480)),
            ("• IMU: 6-axis stabilization", (100, 510)),
            ("• Altimeter: Barometric + GPS", (100, 540)),
        ]
        
        for spec in specs:
            if spec[1]:  # If position is provided
                cv2.putText(frame, spec[0], spec[1], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            else:  # Section header
                cv2.putText(frame, spec[0], (50, spec[1][1] if spec[1] else 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        
        # Add drone illustration
        self.draw_drone_illustration(frame, (self.width - 300, 200))
        
        return frame
    
    def draw_drone_illustration(self, frame, position):
        """Draw a simple drone illustration"""
        x, y = position
        
        # Main body
        cv2.rectangle(frame, (x-40, y-20), (x+40, y+20), (100, 100, 100), -1)
        cv2.rectangle(frame, (x-40, y-20), (x+40, y+20), (255, 255, 255), 2)
        
        # Propellers
        cv2.circle(frame, (x-60, y-40), 15, (80, 80, 80), -1)
        cv2.circle(frame, (x+60, y-40), 15, (80, 80, 80), -1)
        cv2.circle(frame, (x-60, y+40), 15, (80, 80, 80), -1)
        cv2.circle(frame, (x+60, y+40), 15, (80, 80, 80), -1)
        
        # Camera
        cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
        cv2.circle(frame, (x, y), 8, (255, 255, 255), 1)
        
        # Labels
        cv2.putText(frame, "Camera", (x-30, y+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Propellers", (x-40, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def create_simulation_frame(self):
        """Create a simulation frame"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background
        frame.fill((50, 100, 50))
        
        # Update birds
        wind = (0, 0)
        bounds = (self.width, self.height)
        
        # Initialize birds if needed
        if len(self.birds) == 0:
            for i in range(8):
                pos = (np.random.randint(100, self.width-100), np.random.randint(100, self.height-100))
                vel = (np.random.uniform(-2, 2), np.random.uniform(-2, 2))
                self.birds.append(Bird(pos, vel))
        
        # Update and draw birds
        for bird in self.birds:
            bird.update(self.birds, bounds, wind)
            
            # Draw bird
            x, y = int(bird.position[0]), int(bird.position[1])
            color = bird.get_color()
            cv2.circle(frame, (x, y), 8, color, -1)
            cv2.circle(frame, (x, y), 8, (255, 255, 255), 2)
            
            # Draw state indicator
            state_colors = {
                'CRUISING': (0, 255, 0),
                'SOARING': (255, 255, 0),
                'GLIDING': (0, 255, 255),
                'PERCHED': (128, 128, 128),
                'TAKING_OFF': (255, 128, 0)
            }
            state_color = state_colors.get(bird.state, (255, 255, 255))
            cv2.circle(frame, (x+12, y-12), 4, state_color, -1)
        
        # Update and draw UAV
        self.uav.update(self.birds)
        uav_x, uav_y = int(self.uav.position[0]), int(self.uav.position[1])
        cv2.circle(frame, (uav_x, uav_y), 12, (255, 0, 0), -1)
        cv2.circle(frame, (uav_x, uav_y), 12, (255, 255, 255), 2)
        
        # Draw UAV target line if tracking
        if self.uav.target_bird:
            target_x, target_y = int(self.uav.target_bird.position[0]), int(self.uav.target_bird.position[1])
            cv2.line(frame, (uav_x, uav_y), (target_x, target_y), (255, 255, 0), 2)
        
        # Add UI elements
        cv2.putText(frame, "UAV Path Planning Simulation", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Birds: {len(self.birds)}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"UAV Energy: {self.uav.energy:.1f}%", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Frame: {self.frame_count}", (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add legend
        legend_y = self.height - 100
        cv2.putText(frame, "Legend:", (self.width - 200, legend_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.circle(frame, (self.width - 180, legend_y + 20), 6, (255, 0, 0), -1)
        cv2.putText(frame, "UAV", (self.width - 160, legend_y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.circle(frame, (self.width - 180, legend_y + 40), 6, (0, 255, 0), -1)
        cv2.putText(frame, "Birds", (self.width - 160, legend_y + 45), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def create_conclusion_screen(self):
        """Create conclusion screen"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background
        frame.fill(30)
        
        # Title
        cv2.putText(frame, "Demo Complete", (50, 80), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 2)
        
        # Content
        content = [
            "This demonstration showcases:",
            "",
            "• Real-time UAV path planning",
            "• Dynamic bird behavior simulation",
            "• 3D environment visualization",
            "• Energy-efficient navigation",
            "• Target acquisition algorithms",
            "",
            "For more information about the full research project:",
            "",
            "Author: Solomon Makuwa",
            "Email: 202211185@spu.ac.za",
            "Institution: Sol Plaatje University",
            "Supervisors: Lebelo Serutla, Dr Alfred Mwanza"
        ]
        
        y_start = 150
        for i, line in enumerate(content):
            y = y_start + i * 35
            if line.startswith("•"):
                color = (0, 255, 255)
            elif "Author:" in line or "Email:" in line or "Institution:" in line or "Supervisors:" in line:
                color = (255, 255, 0)
            else:
                color = (200, 200, 200)
            cv2.putText(frame, line, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return frame
    
    def generate_video(self):
        """Generate the complete demo video"""
        print("Generating UAV Demo Video...")
        print(f"Output file: {self.output_filename}")
        
        # Section durations (in frames)
        intro_duration = 3 * self.fps  # 3 seconds
        specs_duration = 8 * self.fps  # 8 seconds
        simulation_duration = 15 * self.fps  # 15 seconds
        conclusion_duration = 4 * self.fps  # 4 seconds
        
        total_frames = intro_duration + specs_duration + simulation_duration + conclusion_duration
        
        # Generate video frames
        for frame_num in range(total_frames):
            if frame_num < intro_duration:
                # Intro section
                frame = self.create_title_screen(
                    "UAV Path Planning Demo",
                    "Drone Specifications & Simulation"
                )
            elif frame_num < intro_duration + specs_duration:
                # Specifications section
                frame = self.create_specifications_screen()
            elif frame_num < intro_duration + specs_duration + simulation_duration:
                # Simulation section
                frame = self.create_simulation_frame()
                self.frame_count += 1
            else:
                # Conclusion section
                frame = self.create_conclusion_screen()
            
            # Write frame
            self.video_writer.write(frame)
            
            # Progress indicator
            if frame_num % 30 == 0:
                progress = (frame_num / total_frames) * 100
                print(f"Progress: {progress:.1f}%")
        
        # Release video writer
        self.video_writer.release()
        
        print(f"Video generation complete: {self.output_filename}")
        print(f"Video duration: {total_frames / self.fps:.1f} seconds")
        
        return self.output_filename

def main():
    """Main function to generate the demo video"""
    print("UAV Path Planning Demo Video Generator")
    print("=" * 50)
    
    # Create video generator
    generator = VideoGenerator()
    
    # Generate video
    output_file = generator.generate_video()
    
    print("\nVideo generation completed successfully!")
    print(f"Output file: {output_file}")
    print("\nYou can now share this video to showcase your UAV path planning demo.")

if __name__ == "__main__":
    main() 