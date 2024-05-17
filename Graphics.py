import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser, Toplevel, Label, Button, Scale
import random
import time
import math
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FONT_STYLE = ("Arial", 10, "bold")
FONT_STYLE_SMALL = ("Arial", 8)
# Initial global style settings
SETTINGS = {
    "background_color": "#34495e",
    "line_color": "#2ecc71",
    "city_color": "#e74c3c",
    "text_color": "#ecf0f1",
    "path_width": 2,
    "city_radius": 5,
    "font_style": ("Arial", 10, "bold"),
}

# Global variables
cities = []
zoom_scale = 1.0
offset_x = 0
offset_y = 0

# Utility functions
def distance(city1, city2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def transform_coordinates(x, y):
    """Transform coordinates based on zoom and pan."""
    global zoom_scale, offset_x, offset_y
    return x * zoom_scale + offset_x, y * zoom_scale + offset_y

def reverse_transform_coordinates(x, y):
    """Reverse transform coordinates to original scale."""
    global zoom_scale, offset_x, offset_y
    return (x - offset_x) / zoom_scale, (y - offset_y) / zoom_scale

def apply_settings():
    """Apply color and style settings from SETTINGS dictionary."""
    global SETTINGS
    canvas.config(bg=SETTINGS["background_color"])
    update_paths()

# Main algorithm functions
def solve_tsp_random(cities, extra_points):
    """Solve TSP by creating a random path, optionally with extra revisits."""
    original_cities = list(set(cities))
    path = original_cities[:]
    for _ in range(extra_points):
        path.append(random.choice(original_cities))
    random.shuffle(path)
    return path

def update_paths():
    """Redraw the paths and cities on the canvas based on the current list of cities."""
    canvas.delete("path")
    canvas.delete("city")
    if cities:
        for i in range(len(cities) - 1):
            x1, y1 = transform_coordinates(*cities[i])
            x2, y2 = transform_coordinates(*cities[i+1])
            canvas.create_line(x1, y1, x2, y2, fill=SETTINGS["line_color"], width=SETTINGS["path_width"], tags="path")
        # Close the loop
        x1, y1 = transform_coordinates(*cities[-1])
        x2, y2 = transform_coordinates(*cities[0])
        canvas.create_line(x1, y1, x2, y2, fill=SETTINGS["line_color"], width=SETTINGS["path_width"], tags="path")
        # Draw cities
        for city in cities:
            x, y = transform_coordinates(*city)
            canvas.create_oval(x - SETTINGS["city_radius"], y - SETTINGS["city_radius"], 
                               x + SETTINGS["city_radius"], y + SETTINGS["city_radius"], 
                               fill=SETTINGS["city_color"], outline=SETTINGS["text_color"], tags="city")

def clear_canvas():
    """Clear all cities and paths from the canvas."""
    global cities
    cities = []
    update_paths()

# GUI functions
def draw_city(event):
    """Add a new city at the mouse click location, accounting for zoom and pan."""
    x, y = reverse_transform_coordinates(event.x, event.y)
    cities.append((x, y))
    update_paths()

def undo_last_city():
    """Remove the last added city."""
    if cities:
        cities.pop()
        update_paths()

def zoom(event):
    """Zoom in or out of the canvas view."""
    global zoom_scale, offset_x, offset_y
    scale_factor = 1.1
    if event.delta < 0:  # Zoom out
        scale_factor = 1.0 / scale_factor
    zoom_scale *= scale_factor
    offset_x = event.x - (event.x - offset_x) * scale_factor
    offset_y = event.y - (event.y - offset_y) * scale_factor
    update_paths()

def pan_start(event):
    """Record the initial position for panning."""
    canvas.scan_mark(event.x, event.y)

def pan_move(event):
    """Pan the view based on mouse movement."""
    canvas.scan_dragto(event.x, event.y, gain=1)

def customize_appearance():
    """Open a dialog for customizing appearance settings."""
    global SETTINGS
    new_bg_color = colorchooser.askcolor(color=SETTINGS["background_color"], title="Choose background color")[1]
    if new_bg_color:
        SETTINGS["background_color"] = new_bg_color
    new_line_color = colorchooser.askcolor(color=SETTINGS["line_color"], title="Choose line color")[1]
    if new_line_color:
        SETTINGS["line_color"] = new_line_color

    new_city_color = colorchooser.askcolor(color=SETTINGS["city_color"], title="Choose city color")[1]
    if new_city_color:
        SETTINGS["city_color"] = new_city_color

    new_text_color = colorchooser.askcolor(color=SETTINGS["text_color"], title="Choose text color")[1]
    if new_text_color:
        SETTINGS["text_color"] = new_text_color

    apply_settings()

def show_tutorial():
    """Show an interactive tutorial using message boxes."""
    messagebox.showinfo("Tutorial", "Welcome to the TSP Solver Tutorial!\n\nClick on the canvas to add cities.")
    messagebox.showinfo("Tutorial", "Use the 'Solve Rand' button to solve the TSP with a random path including revisits.")
    messagebox.showinfo("Tutorial", "Use the 'Solve Greedy' button to solve the TSP with the nearest neighbor algorithm, allowing revisits.")
    messagebox.showinfo("Tutorial", "Use the slider to adjust the number of revisits allowed.")
    messagebox.showinfo("Tutorial", "Right-click and drag to pan around the canvas.")
    messagebox.showinfo("Tutorial", "Use the mouse wheel to zoom in and out.")
    
def display_algorithm_time(time_taken):
    canvas.delete("time")
    # Display time with 6 decimal places
    canvas.create_text(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 40, text=f"Time: {time_taken:.6f}s", fill="blue", font=FONT_STYLE, tags="time")

def nearest_neighbor_with_revisits(cities, num_revisits_allowed):
    if not cities:
        return []
    unvisited = set(cities)
    path = [unvisited.pop()]
    while unvisited:
        current_city = path[-1]
        next_city = min(unvisited, key=lambda city: distance(current_city, city))
        path.append(next_city)
        unvisited.remove(next_city)
    for _ in range(num_revisits_allowed):
        insert_pos = random.randint(1, len(path)-1)
        path.insert(insert_pos, random.choice(cities))
    return path

def solve_tsp_random_btn():
    """Button event handler for solving TSP with random path."""
    num_extra_points = numRevisits.get()
    start_time = time.perf_counter()
    solved_path = solve_tsp_random(cities, num_extra_points)
    end_time = time.perf_counter()
    cities[:] = solved_path
    update_paths()
    display_algorithm_time(end_time - start_time)

def solve_tsp_nearest_neighbor_btn():
    """Button event handler for solving TSP with nearest neighbor and revisits."""
    num_revisits_allowed = numRevisits.get()
    start_time = time.perf_counter()
    solved_path = nearest_neighbor_with_revisits(cities, num_revisits_allowed)
    end_time = time.perf_counter()
    cities[:] = solved_path
    update_paths()
    display_algorithm_time(end_time - start_time)

# Setting up the GUI
window = tk.Tk()
window.title("TSP Solver with Enhanced Graphics")
canvas = tk.Canvas(window, width=800, height=600, bg=SETTINGS["background_color"])
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", draw_city)
canvas.bind("<Button-3>", pan_start)
canvas.bind("<B3-Motion>", pan_move)
canvas.bind("<MouseWheel>", zoom)

control_panel = tk.Frame(window, bg="gray")
control_panel.pack(side=tk.RIGHT, fill=tk.Y)

numRevisits = tk.IntVar(value=0)
revisit_slider = tk.Scale(control_panel, from_=0, to=20, orient="horizontal", variable=numRevisits, label="Number of Revisits", font=FONT_STYLE)
revisit_slider.pack()

solve_button = tk.Button(control_panel, text="Solve Rand", command=solve_tsp_random_btn)
solve_button.pack(pady=5)

solve2_button = tk.Button(control_panel, text="Solve Greedy", command=solve_tsp_nearest_neighbor_btn)
solve2_button.pack(pady=5)

clear_button = tk.Button(control_panel, text="Clear", command=clear_canvas)
clear_button.pack(pady=5)

customize_button = tk.Button(control_panel, text="Customize Appearance", command=customize_appearance)
customize_button.pack(pady=5)

tutorial_button = tk.Button(control_panel, text="Show Tutorial", command=show_tutorial)
tutorial_button.pack(pady=5)

undo_button = tk.Button(control_panel, text="Undo", command=undo_last_city)
undo_button.pack(pady=5)

window.mainloop()
