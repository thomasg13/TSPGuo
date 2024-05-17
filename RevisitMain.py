import tkinter as tk
from tkinter.font import Font
import random
import time

# Define colors and styles
BACKGROUND_COLOR = "#34495e"
LINE_COLOR = "#2ecc71"
CITY_COLOR = "#e74c3c"
TEXT_COLOR = "#ecf0f1"
PATH_WIDTH = 2
CITY_RADIUS = 5
FONT_STYLE = ("Arial", 10, "bold")

# Other global constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Function to calculate the Euclidean distance between two points
def distance(city1, city2):
    return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5

# Graphics improvements: Draw more prominent cities and paths
def draw_city(event):
    x, y = event.x, event.y
    if 0 <= x <= WINDOW_WIDTH and 0 <= y <= WINDOW_HEIGHT:
        cities.append((x, y))
        canvas.create_oval(x - CITY_RADIUS, y - CITY_RADIUS, x + CITY_RADIUS, y + CITY_RADIUS, fill=CITY_COLOR, outline=TEXT_COLOR)
        canvas.create_text(x, y - 15, text=str(len(cities)-1), fill=TEXT_COLOR, font=FONT_STYLE)
        update_paths()

def update_paths():
    canvas.delete("path")
    if len(cities) > 1:
        for i in range(len(cities)-1):
            canvas.create_line(cities[i] + cities[i+1], fill=LINE_COLOR, width=PATH_WIDTH, tags="path")
        canvas.create_line(cities[-1] + cities[0], fill=LINE_COLOR, width=PATH_WIDTH, tags="path")  # Close the loop
    display_total_distance(cities)

def display_total_distance(path):
    total_dist = sum(distance(path[i], path[(i+1) % len(path)]) for i in range(len(path)))
    canvas.delete("total_dist")
    canvas.create_text(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 20, text=f"Total Distance: {total_dist:.2f}", fill=TEXT_COLOR, font=FONT_STYLE, tags="total_dist")

def display_algorithm_time(time_taken):
    canvas.delete("time")
    # Display time with 6 decimal places
    canvas.create_text(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 40, text=f"Time: {time_taken:.6f}s", fill=TEXT_COLOR, font=FONT_STYLE, tags="time")

def random_algorithm_with_extra_points(cities, num_extra_points):
    original_cities = list(set(cities))
    path = original_cities[:]
    for _ in range(num_extra_points):
        path.append(random.choice(original_cities))
    random.shuffle(path)
    return path

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

def solve_tsp():
    start_time = time.time()
    num_extra_points = numRevisits.get()
    solved_path = random_algorithm_with_extra_points(cities, num_extra_points)
    end_time = time.time()
    cities[:] = solved_path
    update_paths()
    display_algorithm_time(end_time - start_time)

def solve_tsp_with_nearest_neighbor():
    start_time = time.time()
    num_revisits_allowed = numRevisits.get()
    solved_path = nearest_neighbor_with_revisits(cities, num_revisits_allowed)
    end_time = time.time()
    cities[:] = solved_path
    update_paths()
    display_algorithm_time(end_time - start_time)

def clear_canvas():
    cities.clear()
    canvas.delete("all")

window = tk.Tk()
window.title("TSP Solver with Revisits")

canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", draw_city)

cities = []
numRevisits = tk.IntVar(value=0)

control_panel = tk.Frame(window, bg="gray")
control_panel.pack(side=tk.RIGHT, fill=tk.Y)

revisit_slider = tk.Scale(control_panel, from_=0, to=20, orient="horizontal", variable=numRevisits, label="Number of Revisits", font=FONT_STYLE)
revisit_slider.pack()

solve_button = tk.Button(control_panel, text="Solve Rand", command=solve_tsp)
solve_button.pack(pady=5)

solve2_button = tk.Button(control_panel, text="Solve Greedy", command=solve_tsp_with_nearest_neighbor)
solve2_button.pack(pady=5)

clear_button = tk.Button(control_panel, text="Clear", command=clear_canvas)
clear_button.pack(pady=5)

window.mainloop()
