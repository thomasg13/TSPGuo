import tkinter as tk
import random
import time
from itertools import permutations

# --- GUI Functions ---

def draw_city(event):
    x, y = event.x, event.y
    city_number = len(cities)
    cities.append((x, y))
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
    canvas.create_text(x, y - 10, text=f'{city_number}', fill='red', font=('Arial', 8))

def update_paths():
    canvas.delete("path")  # Remove old paths
    draw_path_segment(0)

def draw_path_segment(i):
    global window  # Declare window as global
    if i < len(cities) - 1:
        canvas.create_line(cities[i], cities[i + 1], tags="path", fill='blue')
        window.after(100, draw_path_segment, i + 1)  # Delay of 100 ms



def solve_tsp(algorithm):
    global cities

    if not cities:
        return  # No cities to solve for

    BRUTE_FORCE_LIMIT = 8

    start_time = time.perf_counter()  # Start high-resolution timer

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

    end_time = time.perf_counter()  # End high-resolution timer

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

# --- TSP Algorithms ---

# [Greedy, Brute Force, Nearest Neighbor, and Random algorithms]

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

def path_length(path):
    """
    Calculate the total length of the path.
    The path is a list of cities, and each city is a tuple of coordinates.
    """
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

def random_algorithm(cities):
    """
    Generate a random path by shuffling the list of cities.
    """
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
                if j - i == 1: continue  # Skip adjacent edges
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


# --- Helper Functions ---

# [Distance and Path Length functions]

# --- Main Application ---

def main():
    global window;
    global canvas, cities, start_city
    cities = []
    start_city = None

    window = tk.Tk()
    window.title("Traveling Salesman Problem")

    canvas = tk.Canvas(window, width=600, height=400, bg='white')
    canvas.pack()
    canvas.bind("<Button-1>", draw_city)
    canvas.bind("<Button-3>", set_start_city)  # Right-click to set start city

    algorithm_var = tk.StringVar(window)
    algorithm_var.set("greedy")  # default value
    algorithm_menu = tk.OptionMenu(window, algorithm_var, "greedy", "brute_force", "nearest_neighbor", "random", "2-opt", "nearest_insertion")
    algorithm_menu.pack()

    btn_solve = tk.Button(window, text="Solve", command=lambda: solve_tsp(algorithm_var.get()))
    btn_solve.pack()

    btn_clear = tk.Button(window, text="Clear", command=clear_canvas)
    btn_clear.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
