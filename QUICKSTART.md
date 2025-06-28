# Quick Start Guide

## Prerequisites

- Python 3.7 or higher
- Git (for cloning)
- GitHub CLI (optional, for repository setup)

## Installation

### Option 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/uav-path-planning-demo.git
cd uav-path-planning-demo

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Install via pip

```bash
pip install uav-path-planning-demo
```

## Running the Demo

### 2D Simulation

```bash
python src/demo_simulation.py
```

**Controls:**

- `a` - Add new bird
- `t` - Add thermal updraft
- `q` - Quit simulation

### 3D Environment Viewer

```bash
python src/environment_viewer.py
```

**Features:**

- Interactive 3D terrain visualization
- Real-time bird swarm movement
- UAV position tracking
- Mouse controls for rotation and zoom

## What You'll See

### 2D Simulation

- Green background representing the environment
- Colored circles representing birds (color indicates energy level)
- Blue circle representing the UAV
- Yellow line showing UAV target tracking
- Real-time performance metrics

### 3D Environment Viewer

- Procedurally generated terrain with realistic lighting
- Green dots representing vegetation
- Red dots representing birds in 3D space
- Blue dot representing the UAV
- Interactive 3D controls

## Bird Behavior States

Birds in the simulation exhibit different behaviors:

- **Green** - High energy, cruising
- **Yellow** - Medium energy, normal flight
- **Orange** - Low energy, seeking rest
- **Red** - Very low energy, may perch soon

## UAV Behavior

The UAV demonstrates:

- Target selection based on proximity and bird energy
- Path planning towards selected targets
- Patrol behavior when no targets are available
- Energy management and consumption

## Customization

You can modify various parameters in the source files:

- `src/bird_simulation.py` - Bird behavior parameters
- `src/uav_controller.py` - UAV control parameters
- `src/environment_viewer.py` - 3D visualization settings

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed

   ```bash
   pip install -r requirements.txt
   ```

2. **Display issues**: Ensure you have proper graphics drivers installed

3. **Performance issues**: Reduce the number of birds or simulation complexity

### Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Ensure all dependencies are correctly installed
3. Try running with fewer birds or simpler settings

## Next Steps

After running the demo:

1. Experiment with different parameters
2. Try the 3D environment viewer
3. Explore the source code to understand the implementation
4. Consider contributing improvements

## Research Contact

For more information about the full research project:

- **Author**: Solomon Makuwa
- **Email**: 202211185@spu.ac.za
- **Institution**: Sol Plaatje University
- **Supervisors**: Lebelo Serutla, Dr Alfred Mwanza
