#!/usr/bin/env python3
"""
Poster Design Elements Generator
Creates visual elements for UAV Path Planning poster
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Circle, Rectangle
import seaborn as sns
from datetime import datetime

class PosterElementGenerator:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.output_dir = "poster_elements"
        
        # Create output directory
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set font to avoid emoji issues
        plt.rcParams['font.family'] = 'DejaVu Sans'
        
    def create_iconography(self):
        """Create iconography section for the poster"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor('#f0f0f0')
        ax.set_facecolor('#f0f0f0')
        
        # Title
        ax.text(0.5, 0.95, 'UAV Path Planning System Components', 
                fontsize=24, fontweight='bold', ha='center', va='center',
                transform=ax.transAxes, color='#2c3e50')
        
        # Define components and their positions
        components = [
            ('AI', 'Edge AI Processing', 0.15, 0.7),
            ('UAV', 'UAV System', 0.35, 0.7),
            ('M', 'Performance Metrics', 0.55, 0.7),
            ('T', 'Target Detection', 0.75, 0.7),
            ('DL', 'Deep Learning', 0.15, 0.4),
            ('C', 'Real-time Communication', 0.35, 0.4),
            ('P', 'High Performance', 0.55, 0.4),
            ('A', 'Adaptive Learning', 0.75, 0.4),
            ('CAM', 'Camera Input', 0.15, 0.1),
            ('CTRL', 'Control System', 0.35, 0.1),
            ('OPT', 'Optimization', 0.55, 0.1),
            ('S', 'Safety Features', 0.75, 0.1)
        ]
        
        # Draw components and labels
        for icon, label, x, y in components:
            # Background circle
            circle = Circle((x, y + 0.1), 0.08, facecolor='white', 
                              edgecolor='#3498db', linewidth=2, alpha=0.8)
            ax.add_patch(circle)
            
            # Icon text
            ax.text(x, y + 0.1, icon, fontsize=16, fontweight='bold', ha='center', va='center',
                   transform=ax.transAxes, color='#3498db')
            
            # Label
            ax.text(x, y - 0.05, label, fontsize=10, fontweight='bold', 
                   ha='center', va='center', transform=ax.transAxes,
                   color='#34495e')
        
        # Remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Save
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/iconography.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Iconography created: poster_elements/iconography.png")
        
    def create_flow_diagram(self):
        """Create flow diagram showing the pipeline"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Title
        ax.text(0.5, 0.95, 'UAV Path Planning Pipeline', 
                fontsize=24, fontweight='bold', ha='center', va='center',
                transform=ax.transAxes, color='#2c3e50')
        
        # Define components
        components = [
            ('CAM', 'Camera Input', 0.1, 0.5, '#e74c3c'),
            ('YOLO', 'YOLO Detection', 0.25, 0.5, '#e67e22'),
            ('SORT', 'DeepSORT Tracking', 0.4, 0.5, '#f39c12'),
            ('DDQN', 'DDQN Agent', 0.55, 0.5, '#27ae60'),
            ('CTRL', 'UAV Control', 0.7, 0.5, '#8e44ad'),
            ('UAV', 'UAV Action', 0.85, 0.5, '#2980b9')
        ]
        
        # Draw components
        for icon, label, x, y, color in components:
            # Background box
            box = FancyBboxPatch((x-0.08, y-0.15), 0.16, 0.3,
                               boxstyle="round,pad=0.02",
                               facecolor=color, edgecolor='white', linewidth=2)
            ax.add_patch(box)
            
            # Icon
            ax.text(x, y + 0.05, icon, fontsize=14, fontweight='bold', ha='center', va='center',
                   transform=ax.transAxes, color='white')
            
            # Label
            ax.text(x, y - 0.08, label, fontsize=9, fontweight='bold', 
                   ha='center', va='center', transform=ax.transAxes,
                   color='white')
        
        # Draw arrows
        for i in range(len(components) - 1):
            x1 = components[i][2] + 0.08
            x2 = components[i+1][2] - 0.08
            y = components[i][3]
            
            # Arrow
            arrow = ConnectionPatch((x1, y), (x2, y), "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=20, fc="#34495e", ec="#34495e",
                                  linewidth=2)
            ax.add_patch(arrow)
            
            # Arrow label
            if i == 0:
                ax.text((x1 + x2)/2, y + 0.2, 'Object Detection', 
                       fontsize=8, ha='center', va='center',
                       transform=ax.transAxes, color='#34495e')
            elif i == 1:
                ax.text((x1 + x2)/2, y + 0.2, 'Multi-Object Tracking', 
                       fontsize=8, ha='center', va='center',
                       transform=ax.transAxes, color='#34495e')
            elif i == 2:
                ax.text((x1 + x2)/2, y + 0.2, 'Reinforcement Learning', 
                       fontsize=8, ha='center', va='center',
                       transform=ax.transAxes, color='#34495e')
            elif i == 3:
                ax.text((x1 + x2)/2, y + 0.2, 'Path Planning', 
                       fontsize=8, ha='center', va='center',
                       transform=ax.transAxes, color='#34495e')
            elif i == 4:
                ax.text((x1 + x2)/2, y + 0.2, 'Execution', 
                       fontsize=8, ha='center', va='center',
                       transform=ax.transAxes, color='#34495e')
        
        # Add performance indicators
        ax.text(0.5, 0.15, 'Real-time Processing | High Accuracy | Adaptive Learning', 
               fontsize=14, fontweight='bold', ha='center', va='center',
               transform=ax.transAxes, color='#27ae60',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#27ae60'))
        
        # Remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Save
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/flow_diagram.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Flow diagram created: poster_elements/flow_diagram.png")
        
    def create_comparison_table(self):
        """Create comparison table highlighting performance gains"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Title
        ax.text(0.5, 0.95, 'Performance Comparison: Our Approach vs Baselines', 
                fontsize=20, fontweight='bold', ha='center', va='center',
                transform=ax.transAxes, color='#2c3e50')
        
        # Define data
        metrics = ['Success Rate (%)', 'Path Efficiency (%)', 'Response Time (ms)', 
                  'Energy Consumption (%)', 'Adaptation Speed']
        our_approach = [95.2, 87.5, 45, 78.3, 'High']
        a_star = [72.1, 65.8, 120, 92.1, 'None']
        vanilla_dqn = [68.4, 71.2, 85, 88.7, 'Low']

        # Transpose data for table: each row is a metric, columns are methods
        table_data = []
        for i, metric in enumerate(metrics):
            table_data.append([
                metric,
                our_approach[i],
                a_star[i],
                vanilla_dqn[i]
            ])
        column_labels = ['Metric', 'Our Approach\n(Hybrid DDQN)', 'A* Algorithm', 'Vanilla DQN']

        # Colors for highlighting
        colors = []
        for i in range(len(metrics)):
            row_colors = ['#ecf0f1', '#d5f4e6', '#fadbd8', '#fdeaa7']
            colors.append(row_colors)

        # Create table
        table = ax.table(cellText=table_data, colLabels=column_labels,
                        cellColours=colors, cellLoc='center',
                        loc='center', bbox=None)

        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 2)

        # Highlight header
        for i in range(len(column_labels)):
            table[(0, i)].set_facecolor('#3498db')
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Highlight our approach as best
        for i in range(1, len(metrics) + 1):
            table[(i, 1)].set_facecolor('#27ae60')
            table[(i, 1)].set_text_props(weight='bold', color='white')

        # Add performance improvement arrows
        improvements = ['+32%', '+33%', '+47%', '+15%', 'N/A']
        for i, improvement in enumerate(improvements):
            if improvement != 'N/A':
                ax.text(0.85, 0.75 - i * 0.1, improvement, 
                       fontsize=10, fontweight='bold', ha='center', va='center',
                       transform=ax.transAxes, color='#27ae60',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='#27ae60'))

        # Add legend
        legend_elements = [
            Rectangle((0, 0), 1, 1, facecolor='#27ae60', label='Best Performance'),
            Rectangle((0, 0), 1, 1, facecolor='#fadbd8', label='Baseline A*'),
            Rectangle((0, 0), 1, 1, facecolor='#fdeaa7', label='Baseline DQN')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.85))

        # Remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Save
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/comparison_table.png', dpi=300, bbox_inches='tight')
        plt.close()

        print("Comparison table created: poster_elements/comparison_table.png")
        
    def create_system_architecture(self):
        """Create system architecture diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Title
        ax.text(0.5, 0.95, 'Hybrid UAV Path Planning System Architecture', 
                fontsize=20, fontweight='bold', ha='center', va='center',
                transform=ax.transAxes, color='#2c3e50')
        
        # Define system layers
        layers = [
            ('UAV', 'UAV Platform', 0.5, 0.85, '#3498db', 0.3, 0.08),
            ('SENS', 'Sensors', 0.2, 0.75, '#e74c3c', 0.15, 0.06),
            ('EDGE', 'Edge Processing', 0.8, 0.75, '#e67e22', 0.15, 0.06),
            ('AI', 'AI Engine', 0.5, 0.65, '#27ae60', 0.25, 0.06),
            ('DEC', 'Decision System', 0.5, 0.55, '#8e44ad', 0.25, 0.06),
            ('CTRL', 'Control System', 0.5, 0.45, '#f39c12', 0.25, 0.06),
            ('PERF', 'Performance Monitor', 0.2, 0.35, '#1abc9c', 0.15, 0.06),
            ('LEARN', 'Learning Module', 0.8, 0.35, '#9b59b6', 0.15, 0.06),
            ('SAFE', 'Safety System', 0.5, 0.25, '#e74c3c', 0.2, 0.06),
            ('COMM', 'Communication', 0.5, 0.15, '#34495e', 0.2, 0.06)
        ]
        
        # Draw layers
        for icon, label, x, y, color, width, height in layers:
            # Background box
            box = FancyBboxPatch((x-width/2, y-height/2), width, height,
                               boxstyle="round,pad=0.01",
                               facecolor=color, edgecolor='white', linewidth=2)
            ax.add_patch(box)
            
            # Icon
            ax.text(x, y + 0.02, icon, fontsize=12, fontweight='bold', ha='center', va='center',
                   transform=ax.transAxes, color='white')
            
            # Label
            ax.text(x, y - 0.02, label, fontsize=8, fontweight='bold', 
                   ha='center', va='center', transform=ax.transAxes,
                   color='white')
        
        # Draw connections
        connections = [
            ((0.5, 0.81), (0.2, 0.78)),  # UAV to Sensors
            ((0.5, 0.81), (0.8, 0.78)),  # UAV to Edge
            ((0.2, 0.72), (0.5, 0.62)),  # Sensors to AI
            ((0.8, 0.72), (0.5, 0.62)),  # Edge to AI
            ((0.5, 0.62), (0.5, 0.52)),  # AI to Decision
            ((0.5, 0.52), (0.5, 0.42)),  # Decision to Control
            ((0.5, 0.42), (0.2, 0.32)),  # Control to Monitor
            ((0.5, 0.42), (0.8, 0.32)),  # Control to Learning
            ((0.2, 0.32), (0.5, 0.22)),  # Monitor to Safety
            ((0.8, 0.32), (0.5, 0.22)),  # Learning to Safety
            ((0.5, 0.22), (0.5, 0.12))   # Safety to Communication
        ]
        
        for (x1, y1), (x2, y2) in connections:
            arrow = ConnectionPatch((x1, y1), (x2, y2), "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=15, fc="#34495e", ec="#34495e",
                                  linewidth=1.5, alpha=0.7)
            ax.add_patch(arrow)
        
        # Add technology stack
        tech_stack = [
            'Python + Rust', 'PyTorch', 'OpenCV', 'ROS2',
            'TensorRT', 'CUDA', 'Real-time Linux'
        ]
        
        for i, tech in enumerate(tech_stack):
            x = 0.1 + (i % 3) * 0.3
            y = 0.05 - (i // 3) * 0.03
            ax.text(x, y, tech, fontsize=9, ha='center', va='center',
                   transform=ax.transAxes, color='#34495e',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='#bdc3c7'))
        
        # Remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Save
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/system_architecture.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("System architecture created: poster_elements/system_architecture.png")
        
    def create_performance_chart(self):
        """Create performance visualization chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Set style
        plt.style.use('default')
        
        # Data
        methods = ['A*', 'Vanilla DQN', 'Our Approach\n(Hybrid DDQN)']
        success_rates = [72.1, 68.4, 95.2]
        response_times = [120, 85, 45]
        energy_consumption = [92.1, 88.7, 78.3]
        
        # Color scheme
        colors = ['#e74c3c', '#f39c12', '#27ae60']
        
        # Success Rate Chart
        bars1 = ax1.bar(methods, success_rates, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        ax1.set_title('Success Rate Comparison (%)', fontsize=16, fontweight='bold', color='#2c3e50')
        ax1.set_ylabel('Success Rate (%)', fontsize=12, color='#34495e')
        ax1.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, value in zip(bars1, success_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{value}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Response Time Chart
        bars2 = ax2.bar(methods, response_times, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        ax2.set_title('Response Time Comparison (ms)', fontsize=16, fontweight='bold', color='#2c3e50')
        ax2.set_ylabel('Response Time (ms)', fontsize=12, color='#34495e')
        ax2.set_ylim(0, 140)
        
        # Add value labels on bars
        for bar, value in zip(bars2, response_times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{value}ms', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Improve appearance
        for ax in [ax1, ax2]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.3)
            ax.tick_params(colors='#34495e')
        
        # Add improvement indicators
        ax1.text(2, 85, '↑ +32%', fontsize=12, fontweight='bold', color='#27ae60',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#27ae60'))
        
        ax2.text(2, 35, '↓ -47%', fontsize=12, fontweight='bold', color='#27ae60',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#27ae60'))
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/performance_chart.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Performance chart created: poster_elements/performance_chart.png")
        
    def generate_all_elements(self):
        """Generate all poster elements"""
        print("Generating Poster Design Elements...")
        print("=" * 50)
        
        self.create_iconography()
        self.create_flow_diagram()
        self.create_comparison_table()
        self.create_system_architecture()
        self.create_performance_chart()
        
        print("\nAll poster elements generated successfully!")
        print("Files saved in: poster_elements/")
        print("\nGenerated files:")
        print("- iconography.png")
        print("- flow_diagram.png")
        print("- comparison_table.png")
        print("- system_architecture.png")
        print("- performance_chart.png")

def main():
    """Main function to generate all poster elements"""
    print("UAV Path Planning Poster Design Elements Generator")
    print("=" * 60)
    
    # Create generator
    generator = PosterElementGenerator()
    
    # Generate all elements
    generator.generate_all_elements()
    
    print("\nPoster elements ready for use!")
    print("You can now incorporate these images into your poster design.")

if __name__ == "__main__":
    main() 