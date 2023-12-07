import matplotlib.pyplot as plt
import random

def generate_random_points(num_points=10):
    """Generate random x, y coordinates."""
    return [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(num_points)]

def plot_points_with_lines(points):
    """Plot points and connect them with lines."""
    # Extract x and y coordinates from the points
    x_coords, y_coords = zip(*points)
    
    # Plot the points
    plt.scatter(x_coords, y_coords, color='blue', s=50, zorder=5)
    
    # Annotate each point with a label
    for i, (x, y) in enumerate(points):
        plt.text(x, y, f'City {i}', fontsize=9, ha='right')
    
    # Connect the points with lines
    plt.plot(x_coords, y_coords, color='grey', linestyle='-', linewidth=1, zorder=1)
    
    # Add the last connection to the first city to complete the loop (TSP-style)
    plt.plot([x_coords[-1], x_coords[0]], [y_coords[-1], y_coords[0]], color='grey', linestyle='-', linewidth=1, zorder=1)
    
    plt.title('Random Cities for TSP')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

if __name__ == "__main__":
    points = generate_random_points()
    plot_points_with_lines(points)
