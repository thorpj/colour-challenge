import secrets
import random
import inspect
import json
import os


def shuffle_list(lst):
    # Randomly sort the list
    seed = secrets.choice(range(1, 5000000))
    random.Random(seed).shuffle(lst)
    return lst


def generate_coordinates(x_max, y_max):
    # Generate a list of coordinates
    coordinates = []
    for x in range(0, x_max):
        for y in range(0, y_max):
            coordinates.append((x, y))
    return coordinates


def generate_colours(Colour):
    # Generate a list of colours
    colours = []
    for r in range(1, 33):
        for g in range(1, 33):
            for b in range(1, 33):
                colours.append(Colour(r, g, b))
    return colours


def generate_algorithms():
    # Generate a list of names of algorithm functions
    import colours
    algorithms = inspect.getmembers(colours, inspect.isfunction)
    algorithms = [algorithm[0] for algorithm in algorithms if algorithm[0].startswith("alg_")]
    return algorithms


