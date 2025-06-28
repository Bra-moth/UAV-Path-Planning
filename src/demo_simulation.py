#!/usr/bin/env python3
"""
UAV Path Planning Simulation Demo
A demonstration of UAV path planning and target acquisition simulation
"""

import cv2
import numpy as np
import time
from typing import List, Tuple
import random
import math
from bird_simulation import Bird
from uav_controller import UAVController

def calculate_movement(current_pos, target_pos, speed=5):
    """Calculate UAV movement vector towards target"""
    if not target_pos:
        return current_pos
        
    cx, cy = current_pos
    tx, ty = target_pos
    
    # Calculate direction vector
    dx = tx - cx
    dy = ty - cy
    
    # Normalize and scale by speed
    distance = np.sqrt(dx**2 + dy**2)
    if distance < speed:  # If very close to target
        return target_pos
    
    dx = (dx / distance) * speed
    dy = (dy / distance) * speed
    
    # Return new position
    return (int(cx + dx), int(cy + dy))

def run_demo_simulation():
    """Run the main demo simulation"""
    print("Starting UAV Path Planning Demo Simulation...")
    print("Controls: 'a' - Add bird, 't' - Add thermal, 'q' - Quit")
    
    # Initialize simulation parameters
    width, height = 800, 600
    screen = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Initialize birds
    birds = []
    for i in range(5):
        pos = (random.randint(100, 700), random.randint(100, 500))
        vel = (random.uniform(-2, 2), random.uniform(-2, 2))
        birds.append(Bird(pos, vel))
    
    # Initialize UAV
    uav = UAVController((width//2, height//2))
    
    # Simulation loop
    frame_count = 0
    start_time = time.time()
    
    while True:
        # Clear screen
        screen.fill((50, 100, 50))  # Green background
        
        # Update birds
        wind = (0, 0)  # No wind for demo
        bounds = (width, height)
        for bird in birds:
            bird.update(birds, bounds, wind)
            
            # Draw bird
            x, y = int(bird.position[0]), int(bird.position[1])
            color = bird.get_color()
            cv2.circle(screen, (x, y), 8, color, -1)
            cv2.circle(screen, (x, y), 8, (255, 255, 255), 2)
            
            # Draw state indicator
            state_colors = {
                'CRUISING': (0, 255, 0),
                'SOARING': (255, 255, 0),
                'GLIDING': (0, 255, 255),
                'PERCHED': (128, 128, 128),
                'TAKING_OFF': (255, 128, 0)
            }
            state_color = state_colors.get(bird.state, (255, 255, 255))
            cv2.circle(screen, (x+12, y-12), 4, state_color, -1)
        
        # Update UAV
        uav.update(birds)
        
        # Draw UAV
        uav_x, uav_y = int(uav.position[0]), int(uav.position[1])
        cv2.circle(screen, (uav_x, uav_y), 12, (255, 0, 0), -1)
        cv2.circle(screen, (uav_x, uav_y), 12, (255, 255, 255), 2)
        
        # Draw UAV target line if tracking
        if uav.target_bird:
            target_x, target_y = int(uav.target_bird.position[0]), int(uav.target_bird.position[1])
            cv2.line(screen, (uav_x, uav_y), (target_x, target_y), (255, 255, 0), 2)
        
        # Draw UI elements
        cv2.putText(screen, f"Birds: {len(birds)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(screen, f"UAV Energy: {uav.energy:.1f}%", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(screen, f"Frame: {frame_count}", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Calculate and display FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            cv2.putText(screen, f"FPS: {fps:.1f}", (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display controls
        cv2.putText(screen, "Controls: 'a' - Add bird, 't' - Add thermal, 'q' - Quit", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Show simulation
        cv2.imshow("UAV Path Planning Demo", screen)
        
        # Handle key presses
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('a'):
            # Add new bird
            pos = (random.randint(100, 700), random.randint(100, 500))
            vel = (random.uniform(-2, 2), random.uniform(-2, 2))
            birds.append(Bird(pos, vel))
            print(f"Added bird. Total birds: {len(birds)}")
        elif key == ord('t'):
            # Add thermal updraft (visual effect)
            thermal_x = random.randint(100, 700)
            thermal_y = random.randint(100, 500)
            cv2.circle(screen, (thermal_x, thermal_y), 30, (0, 255, 255), 2)
            cv2.putText(screen, "THERMAL", (thermal_x-30, thermal_y-40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            print(f"Added thermal updraft at ({thermal_x}, {thermal_y})")
    
    cv2.destroyAllWindows()
    print("Demo simulation completed.")

if __name__ == "__main__":
    run_demo_simulation() 