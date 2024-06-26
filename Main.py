import tkinter as tk
from tkinter.font import Font
from tkinter import IntVar
import random
import time
from itertools import permutations

# Graphics

def draw_city(event):
    x, y = event.x, event.y
    city_number = len(cities)
    cities.append((x, y))
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='white')
    canvas.create_text(x, y - 10, text=f'{city_number}', fill='black', font=('Arial', 10))

def update_paths():
    canvas.delete("path")  # removes old paths
    draw_path_segment(0)

def draw_path_segment(i):
    global window  # windows must be global
    if i < len(cities) - 1:
        canvas.create_line(cities[i], cities[i + 1], tags="path", fill='white')
        X = algorithm_speed_var.get()
        window.after(100, draw_path_segment, i + 1)  # Delay depending on algrotihm speed



def solve_tsp(algorithm):
    global cities

    if not cities:
        return  # edge case, no cities

    BRUTE_FORCE_LIMIT = 8

    start_time = time.perf_counter()  # timer more precise, more decimal values

    # Select and run the algorithm
    if algorithm == 'greedy':
        solved_path = greedy_algorithm(cities)
    elif algorithm == 'brute_force':
        if len(cities) <= BRUTE_FORCE_LIMIT:
            solved_path = brute_force_algorithm(cities)
        else:
            print(f"Brute force not recommended for more than {BRUTE_FORCE_LIMIT} cities.")
            return
    elif algorithm == 'nearest_neighbor':
        solved_path = nearest_neighbor_algorithm(cities, start_city)
    elif algorithm == 'random':
        solved_path = random_algorithm(cities)
    elif algorithm == '2-opt':
        solved_path = two_opt(cities)
    elif algorithm == 'nearest_insertion':
        solved_path = nearest_insertion_algorithm(cities)
    else:
        solved_path = cities.copy()

    end_time = time.perf_counter()  # stops timer

    elapsed_time = end_time - start_time
    total_distance = path_length(solved_path)

    if solved_path:
        cities = solved_path
        update_paths()
        print(f"Algorithm: {algorithm}, Time: {elapsed_time:.6f} seconds, Total Distance: {total_distance}")
    else:
        print("Error: No solution found")

def clear_canvas():
    global cities
    cities = []
    canvas.delete("all")

def set_start_city(event):
    global start_city
    start_city = (event.x, event.y)
    canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, outline='green', width=2)

# Algorithms
# Greedy, Brute Force, Nearest Neighbor, Random, 2-Opt, Nearest Insertion

def greedy_algorithm(cities):
    if len(cities) < 2:
        return cities
    unvisited = cities[:]
    path = [unvisited.pop(0)]
    while unvisited:
        nearest = min(unvisited, key=lambda city: distance(path[-1], city))
        path.append(nearest)
        unvisited.remove(nearest)
    return path

def brute_force_algorithm(cities):
    if len(cities) < 2:
        return cities
    shortest_path = None
    min_distance = float('inf')
    for path in permutations(cities):
        current_distance = path_length(path)
        if current_distance < min_distance:
            min_distance = current_distance
            shortest_path = path
    return list(shortest_path)

def path_length(path): # helper method, calculates path length
    if len(path) < 2:
        return 0
    return sum(distance(path[i], path[i + 1]) for i in range(len(path) - 1))


def nearest_neighbor_algorithm(cities, start_city=None):
    if len(cities) < 2:
        return cities
    if not start_city:
        start_city = random.choice(cities)
    path = [start_city]
    unvisited = set(cities)
    unvisited.remove(start_city)
    while unvisited:
        nearest = min(unvisited, key=lambda city: distance(path[-1], city))
        path.append(nearest)
        unvisited.remove(nearest)
    return path

def random_algorithm(cities): # random path by shuffling list of cities
    path = cities[:]
    random.shuffle(path)
    return path

def two_opt(cities):
    best = cities
    improved = True
    while improved:
        improved = False
        for i in range(1, len(cities) - 2):
            for j in range(i + 1, len(cities)):
                if j - i == 1: continue  # Skips adjacent edges
                new_path = best[:i] + best[i:j][::-1] + best[j:]
                if path_length(new_path) < path_length(best):
                    best = new_path
                    improved = True
                    break
            if improved:
                break
    return best

def nearest_insertion_algorithm(cities):
    if len(cities) < 3:
        return cities
    path = [cities[0], cities[1], cities[0]]
    unvisited = set(cities[2:])
    while unvisited:
        nearest_city, insertion_index = None, None
        min_increase = float('inf')
        for city in unvisited:
            for i in range(1, len(path)):
                increase = distance(city, path[i - 1]) + distance(city, path[i]) - distance(path[i - 1], path[i])
                if increase < min_increase:
                    nearest_city, insertion_index, min_increase = city, i, increase
        path.insert(insertion_index, nearest_city)
        unvisited.remove(nearest_city)
    return path[:-1]


def distance(city1, city2):
    return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5


def add_controls():
    global allow_revisits_var
    allow_revisits_var = tk.BooleanVar(value=False)  # Default: revisits not allowed

    allow_revisits_checkbox = tk.Checkbutton(window, text="Allow Revisits", variable=allow_revisits_var)
    allow_revisits_checkbox.pack()

def add_sliders():
    global max_distance_var, algorithm_speed_var, num_salesmen_var, value
    custom_font = Font(family="Helvetica", size=10) # weight="bold" for bold fonts

    max_distance_var = tk.IntVar(value=100)  # Default max distance
    algorithm_speed_var = tk.IntVar(value=50)  # Default speed (percent)
    num_salesmen_var = tk.IntVar(value=1)  # Default number of salesmen for mTSP
    
    max_distance_slider = tk.Scale(window, from_=0, to=500, label="Max Distance", orient="horizontal", variable=max_distance_var, font=custom_font)
    max_distance_slider.pack()
    
    algorithm_speed_var = tk.IntVar(value=0)
    algorithm_speed_slider = tk.Scale(window, from_=1, to=100, label="Algorithm Speed (%)", orient="horizontal", variable=algorithm_speed_var, font=custom_font)
    value = algorithm_speed_var.get()
    algorithm_speed_slider.pack()
    
    num_salesmen_slider = tk.Scale(window, from_=1, to=10, label="Number of Salesmen", orient="horizontal", variable=num_salesmen_var, font=custom_font)
    num_salesmen_slider.pack()

# Main

def main():
    global window;
    global canvas, cities, start_city
    cities = []
    start_city = None

    window = tk.Tk()
    window.title("Traveling Salesman Problem")

    canvas = tk.Canvas(window, width=600, height=400, bg='light green')
    canvas.pack()
    canvas.bind("<Button-1>", draw_city)
    canvas.bind("<Button-3>", set_start_city)  # Right-click to set start city, not working atm

    add_controls()  # Add the revisit checkbox
    add_sliders()   # Add the sliders
    
    algorithm_var = tk.StringVar(window)
    algorithm_var.set("greedy")  # Current default value
    algorithm_menu = tk.OptionMenu(window, algorithm_var, "greedy", "brute_force", "nearest_neighbor", "random", "2-opt", "nearest_insertion")
    algorithm_menu.pack()

    btn_solve = tk.Button(window, text="Solve", command=lambda: solve_tsp(algorithm_var.get()))
    btn_solve.pack()

    btn_clear = tk.Button(window, text="Clear", command=clear_canvas)
    btn_clear.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
