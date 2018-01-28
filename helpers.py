import secrets
import random
import inspect
import json
import os


def shuffle_list(lst):
    seed = secrets.choice(range(1, 5000000))
    random.Random(seed).shuffle(lst)
    return lst


def generate_coordinates(x_max, y_max):
    coordinates = []
    for x in range(0, x_max):
        for y in range(0, y_max):
            coordinates.append((x, y))
    return coordinates


def generate_colours(Colour):
    colours = []
    for r in range(1, 33):
        for g in range(1, 33):
            for b in range(1, 33):
                colours.append(Colour(r, g, b))
    return colours


def generate_algorithms():
    import colours
    algorithms = inspect.getmembers(colours, inspect.isfunction)
    algorithms = [algorithm[0] for algorithm in algorithms if algorithm[0].startswith("alg_")]
    return algorithms


def read_config():
    filename = "config.json"
    path = os.path.join(".", filename)
    if os.path.exists(path):
        pass
    elif os.path.exists(os.path.join("..", filename)):
        path = os.path.join("..", filename)
    else:
        path = os.path.join("..", "..", filename)
    try:
        with open(path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        return {"image_width": 256, "image_height": 128}
