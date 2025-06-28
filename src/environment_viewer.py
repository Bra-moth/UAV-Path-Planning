"""
3D Environment Viewer for UAV Path Planning Demo
Simplified 3D visualization for demonstration purposes
"""

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
import matplotlib.colors as colors

class TerrainGenerator:
    """Simplified terrain generator for demo purposes"""
    
    def __init__(self, size=100, resolution=50):
        self.size = size
        self.resolution = resolution
        self.generate_terrain()
        self.generate_vegetation()
        
    def generate_terrain(self):
        """Generate terrain using simplified Perlin noise"""
        x = np.linspace(-self.size/2, self.size/2, self.resolution)
        y = np.linspace(-self.size/2, self.size/2, self.resolution)
        self.X, self.Y = np.meshgrid(x, y)
        
        # Generate terrain using multiple frequency components
        self.Z = (
            self.perlin_noise(self.X, self.Y, scale=50) * 15 +  # Large features
            self.perlin_noise(self.X, self.Y, scale=20) * 5 +   # Medium features
            self.perlin_noise(self.X, self.Y, scale=5) * 2      # Small features
        )
        
        # Add some flat areas for agricultural fields
        mask = np.abs(self.perlin_noise(self.X, self.Y, scale=30)) < 0.3
        self.Z[mask] = self.Z[mask] * 0.2
        
    def perlin_noise(self, x, y, scale=10):
        """Simplified Perlin-like noise generation"""
        x = x / scale
        y = y / scale
        
        # Create grid points
        x0 = np.floor(x).astype(int)
        x1 = x0 + 1
        y0 = np.floor(y).astype(int)
        y1 = y0 + 1
        
        # Random gradients
        np.random.seed(42)  # For consistent terrain
        angles = 2 * np.pi * np.random.rand(100, 100)
        gradients = np.stack([np.cos(angles), np.sin(angles)], axis=-1)
        
        # Interpolation weights
        sx = x - x0
        sy = y - y0
        
        # Interpolate
        n0 = self.gradient(gradients[x0 % 99, y0 % 99], x - x0, y - y0)
        n1 = self.gradient(gradients[x1 % 99, y0 % 99], x - x1, y - y0)
        ix0 = self.lerp(n0, n1, sx)
        
        n0 = self.gradient(gradients[x0 % 99, y1 % 99], x - x0, y - y1)
        n1 = self.gradient(gradients[x1 % 99, y1 % 99], x - x1, y - y1)
        ix1 = self.lerp(n0, n1, sx)
        
        return self.lerp(ix0, ix1, sy)
        
    def gradient(self, grad, x, y):
        return grad[..., 0] * x + grad[..., 1] * y
        
    def lerp(self, a, b, x):
        return a + x * (b - a)
        
    def generate_vegetation(self):
        """Generate vegetation positions"""
        num_trees = 50
        mask = np.abs(self.Z) < 10  # Only place trees on relatively flat ground
        possible_positions = np.column_stack((self.X[mask], self.Y[mask], self.Z[mask]))
        
        if len(possible_positions) > num_trees:
            indices = np.random.choice(len(possible_positions), num_trees, replace=False)
            self.tree_positions = possible_positions[indices]
        else:
            self.tree_positions = possible_positions

class BirdSwarm:
    """Simplified bird swarm for 3D visualization"""
    
    def __init__(self, num_birds=10, bounds=(-50, 50)):
        self.num_birds = num_birds
        self.bounds = bounds
        # Initialize random positions for birds
        self.positions = np.random.uniform(
            low=bounds[0], 
            high=bounds[1], 
            size=(num_birds, 3)
        )
        # Set minimum height for birds
        self.positions[:, 2] = np.random.uniform(30, 80, num_birds)
        # Initialize random velocities
        self.velocities = np.random.uniform(-1, 1, (num_birds, 3))
        
    def update(self):
        """Update bird positions"""
        # Update positions based on velocities
        self.positions += self.velocities
        
        # Add some random movement
        self.velocities += np.random.uniform(-0.1, 0.1, (self.num_birds, 3))
        
        # Limit velocity magnitude
        velocity_magnitudes = np.linalg.norm(self.velocities, axis=1)
        for i in range(self.num_birds):
            if velocity_magnitudes[i] > 2:
                self.velocities[i] = self.velocities[i] / velocity_magnitudes[i] * 2
        
        # Keep birds within bounds
        for i in range(3):
            mask = self.positions[:, i] < self.bounds[0]
            self.positions[mask, i] = self.bounds[0]
            self.velocities[mask, i] *= -1
            
            mask = self.positions[:, i] > self.bounds[1]
            self.positions[mask, i] = self.bounds[1]
            self.velocities[mask, i] *= -1
        
        # Keep minimum and maximum height
        self.positions[:, 2] = np.clip(self.positions[:, 2], 30, 80)

class EnvironmentViewer(QMainWindow):
    """3D Environment Viewer for UAV Path Planning Demo"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAV Path Planning 3D Environment Demo")
        self.setGeometry(100, 100, 1200, 900)

        # Create the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create the matplotlib figure
        self.figure = Figure(figsize=(12, 9))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create 3D axes
        self.ax = self.figure.add_subplot(111, projection='3d')
        
        # Initialize environment
        self.terrain = TerrainGenerator()
        
        # Initialize bird swarm
        self.bird_swarm = BirdSwarm(num_birds=15)
        
        # Initialize UAV position
        self.uav_position = np.array([0, 0, 20])
        
        # Setup animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(100)  # Update every 100ms
        
        self.setup_plot()

    def setup_plot(self):
        """Setup the 3D plot"""
        # Set labels and title
        self.ax.set_xlabel('X (meters)')
        self.ax.set_ylabel('Y (meters)')
        self.ax.set_zlabel('Z (meters)')
        self.ax.set_title('UAV Path Planning 3D Environment Demo')

        # Set limits
        self.ax.set_xlim([-50, 50])
        self.ax.set_ylim([-50, 50])
        self.ax.set_zlim([0, 100])

        # Add terrain with improved coloring and lighting
        ls = LightSource(azdeg=315, altdeg=45)
        rgb = ls.shade(self.terrain.Z, plt.cm.terrain, vert_exag=0.3)
        self.terrain_surface = self.ax.plot_surface(
            self.terrain.X, 
            self.terrain.Y, 
            self.terrain.Z,
            facecolors=rgb,
            alpha=1.0,
            antialiased=True
        )

        # Add vegetation
        if hasattr(self.terrain, 'tree_positions') and len(self.terrain.tree_positions) > 0:
            self.ax.scatter(
                self.terrain.tree_positions[:, 0],
                self.terrain.tree_positions[:, 1],
                self.terrain.tree_positions[:, 2],
                c='green', s=20, alpha=0.7, label='Vegetation'
            )

        # Add birds
        self.bird_scatter = self.ax.scatter(
            self.bird_swarm.positions[:, 0],
            self.bird_swarm.positions[:, 1],
            self.bird_swarm.positions[:, 2],
            c='red', s=50, alpha=0.8, label='Birds'
        )

        # Add UAV
        self.uav_scatter = self.ax.scatter(
            [self.uav_position[0]], [self.uav_position[1]], [self.uav_position[2]],
            c='blue', s=100, alpha=0.9, label='UAV'
        )

        # Add legend
        self.ax.legend()

    def update_animation(self):
        """Update animation frame"""
        # Update bird positions
        self.bird_swarm.update()
        
        # Update bird scatter plot
        self.bird_scatter._offsets3d = (
            self.bird_swarm.positions[:, 0],
            self.bird_swarm.positions[:, 1],
            self.bird_swarm.positions[:, 2]
        )
        
        # Update UAV position (simple movement)
        self.uav_position[0] += np.random.uniform(-0.5, 0.5)
        self.uav_position[1] += np.random.uniform(-0.5, 0.5)
        self.uav_position[2] = np.clip(self.uav_position[2] + np.random.uniform(-0.2, 0.2), 15, 25)
        
        # Keep UAV within bounds
        self.uav_position[0] = np.clip(self.uav_position[0], -45, 45)
        self.uav_position[1] = np.clip(self.uav_position[1], -45, 45)
        
        # Update UAV scatter plot
        self.uav_scatter._offsets3d = (
            [self.uav_position[0]], 
            [self.uav_position[1]], 
            [self.uav_position[2]]
        )
        
        # Redraw canvas
        self.canvas.draw()

def main():
    """Main function to run the 3D environment viewer"""
    app = QApplication(sys.argv)
    viewer = EnvironmentViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 