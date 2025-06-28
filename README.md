# UAV Path Planning Simulation Demo

A demonstration of UAV path planning and target acquisition simulation in a 3D environment.

## Overview

This demo showcases a UAV simulation system that demonstrates:

- 3D environment visualization with realistic terrain
- Bird swarm behavior simulation
- UAV path planning and navigation
- Real-time visualization and interaction

## Features

### 🎯 Interactive Simulation

- Real-time 3D visualization
- Dynamic bird swarm behavior
- UAV navigation and path planning
- Interactive controls for adding birds and thermal updrafts

### 🌍 3D Environment

- Procedurally generated terrain using Perlin noise
- Realistic vegetation and structure placement
- Dynamic lighting and shading effects
- Configurable environment parameters

### 🐦 Bird Behavior Simulation

- Realistic flocking behavior
- Energy-based state management (cruising, soaring, gliding, perched)
- Thermal updraft detection and utilization
- Natural movement patterns

### 🚁 UAV Control

- Physics-based movement simulation
- Target tracking and prediction
- Obstacle avoidance
- Energy-efficient path planning

## Installation

### Prerequisites

- Python 3.7 or higher
- Virtual environment (recommended)

### Quick Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/uav-path-planning-demo.git
cd uav-path-planning-demo
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the simulation:

```bash
python src/demo_simulation.py
```

## Usage

### Basic Simulation

```bash
python src/demo_simulation.py
```

### Controls

- **'a'** - Add new bird to the simulation
- **'t'** - Add thermal updraft
- **'q'** - Quit simulation
- **Mouse** - Rotate and zoom the 3D view

### 3D Environment Viewer

```bash
python src/environment_viewer.py
```

## Project Structure

```
├── src/
│   ├── demo_simulation.py      # Main simulation demo
│   ├── environment_viewer.py   # 3D environment visualization
│   ├── bird_simulation.py      # Bird behavior simulation
│   ├── uav_controller.py       # UAV control logic
│   └── terrain_generator.py    # Terrain generation
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Demo Features

### Real-time Visualization

- 3D terrain with realistic lighting
- Dynamic bird movement with flocking behavior
- UAV path visualization
- Performance metrics display

### Interactive Elements

- Add birds dynamically during simulation
- Create thermal updrafts for bird soaring
- Real-time parameter adjustment
- Multiple visualization modes

### Performance Monitoring

- Frame rate display
- Bird count tracking
- UAV performance metrics
- Memory usage monitoring

## Technical Details

### Environment Generation

- Perlin noise-based terrain generation
- Multiple frequency components for realistic landscapes
- Vegetation and structure placement algorithms
- Dynamic lighting and shadow effects

### Bird Behavior

- State-based behavior system (cruising, soaring, gliding, perched)
- Energy management and consumption
- Flocking algorithms with separation, alignment, and cohesion
- Thermal updraft detection and utilization

### UAV Control

- Physics-based movement simulation
- Target prediction algorithms
- Obstacle avoidance
- Energy-efficient path planning

## Contributing

This is a demo repository showcasing UAV path planning simulation capabilities. For research collaborations or commercial inquiries, please contact the project maintainers.

## License

This demo is provided for educational and demonstration purposes. The underlying research and proprietary algorithms are protected by intellectual property rights.

## Acknowledgments

- Sol Plaatje University, Department of Computer Science and Information Technology
- Research supervisors: Lebelo Serutla and Dr Alfred Mwanza
- Academic research project on hybrid UAV path planning systems

## Contact

For more information about the full research project or collaboration opportunities, please contact the research team.

---

**Note:** This is a demonstration version of the UAV path planning system. The full research implementation includes additional proprietary algorithms and advanced features not shown in this demo.
