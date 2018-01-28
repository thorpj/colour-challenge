from PIL import Image
import helpers

config = helpers.read_config()


class Colour:
    def __init__(self, red, green, blue):
        """
        :param red: component of rgb [0 to 31 inclusive].
        :param green: component of rgb [0 to 31 inclusive].
        :param blue: component of rgb [0 to 31 inclusive].
        :var _x: internal variable for x, x coordinate for colour.
        :var _y: internal variable for y, y coordinate for colour.
        """
        self.red = red * 8
        self.green = green * 8
        self.blue = blue * 8
        self._x = None
        self._y = None

    def __eq__(self, other):
        return self.rgb == other.rgb

    def __repr__(self):
        return "({}, {}, {})".format(self.red, self.green, self.blue)

    def __hash__(self):
        return hash(str(self))

    def rgb(self):
        return self.red, self.green, self.blue

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Canvas:
    def __init__(self, x_size, y_size):
        """
        :param x_size: Width of the canvas.
        :param y_size: Height of the canvas.
        """
        self.x_size = x_size
        self.y_size = y_size
        self.pixels = []
        self.image = Image.new('RGB', (x_size, y_size))
        self.image_contents = self.image.load()

    def add(self, colour):
        self.pixels.append(colour)

    def generate(self):
        for pixel in self.pixels:
            self.image_contents[pixel.x, pixel.y] = pixel.rgb()
        return self.image

    def generate_from_list(self, colours, coordinates):
        for colour, coordinates in zip(colours, coordinates):
            colour.x = coordinates[0]
            colour.y = coordinates[1]
            self.image_contents[colour.x, colour.y] = colour.rgb()

    def save(self, filename):
        ext = (filename.split("."))[-1].upper()
        self.image.save(filename, ext)


def alg_sort_by_component_sum(x_max, y_max, reverse=False):
    """
    Sort by the sum of the red, blue and green components of each colour.
    :param x_max:
    :param y_max:
    :param reverse:
    """
    x = 0
    y = 0
    coordinates = []
    for i in range(0, config["image_width"] * config["image_height"]):
        if x >= x_max:
            x = 0
            y += 1
        if y >= y_max:
            y = 0
        coordinates.append((x, y))
        x += 1

    colours = helpers.generate_colours(Colour)
    colours.sort(key=lambda colour: (colour.red + colour.green + colour.blue), reverse=reverse)

    return colours, coordinates


def alg_sort_by_component_sum_reverse(x_max, y_max):
    """
    Reverse sort by the sum of the red, blue and green components of each colour.
    :param x_max:
    :param y_max:
    """
    return alg_sort_by_component_sum(x_max, y_max, reverse=True)


def alg_sort_by_component_difference(x_max, y_max, reverse=False):
    """
    Sort by the difference of the red, blue and green components of each colour.
    :param x_max:
    :param y_max:
    :param reverse:
    """
    x = 0
    y = 0
    coordinates = []
    for i in range(0, config["image_width"] * config["image_height"]):
        if x >= x_max:
            x = 0
            y += 1
        if y >= y_max:
            y = 0
        coordinates.append((x, y))
        x += 1

    colours = helpers.generate_colours(Colour)
    colours.sort(key=lambda colour: (colour.red - colour.green - colour.blue), reverse=reverse)

    return colours, coordinates


def alg_sort_by_component_difference_reverse(x_max, y_max):
    """
    Reverse sort by the difference of the red, blue and green components of each colour.
    :param x_max:
    :param y_max:
    """
    return alg_sort_by_component_difference(x_max, y_max, reverse=True)


def alg_sort_by_coordinate_sum(x_max, y_max, reverse=False):
    """
    Sort by the sum of the x and y coordinates of each colour.
    :param x_max:
    :param y_max:
    """
    x = 0
    y = 0
    coordinates = []
    colours = helpers.generate_colours(Colour)

    for colour in colours:
        if x >= x_max:
            x = 0
            y += 1
        if y >= y_max:
            y = 0
        coordinates.append((x, y))
        colour.x = x
        colour.y = y
        x += 1

    colours.sort(key=lambda colour: (colour.x + colour.y), reverse=reverse)
    return colours, coordinates


def alg_sort_by_coordinate_sum_reverse(x_max, y_max):
    """
    Reverse sort by the sum of the x and y cooridnates of each colour.
    :param x_max:
    :param y_max:
    """
    return alg_sort_by_coordinate_sum(x_max, y_max, reverse=True)


def alg_sort_by_coordinate_x(x_max, y_max, reverse=False):
    """
    Sort by the x coordinate of each colour.
    :param x_max:
    :param y_max:
    """
    x = 0
    y = 0
    coordinates = []
    colours = helpers.generate_colours(Colour)

    for colour in colours:
        if x >= x_max:
            x = 0
            y += 1
        if y >= y_max:
            y = 0
        coordinates.append((x, y))
        colour.x = x
        colour.y = y
        x += 1

    colours.sort(key=lambda colour: (colour.x), reverse=reverse)
    return colours, coordinates


def alg_random(x_max, y_max):
    """
    Colours and coordinates are (psuedo) randomised
    :param x_max:
    :param y_max:
    """
    colours = helpers.shuffle_list(helpers.generate_colours(Colour))
    coordinates = helpers.shuffle_list(helpers.generate_coordinates(x_max, y_max))
    return colours, coordinates


def alg_reverse_red(x_max, y_max):
    """
    Red component is reversed
    :param x_max:
    :param y_max:
    """
    x = 0
    y = 0
    colours = []
    coordinates = []

    for r in range(32, 0, -1):
        for g in range(1, 33):
            for b in range(1, 33):
                if x >= x_max:
                    x = 0
                    y += 1
                if y >= y_max:
                    y = 0
                colours.append(Colour(r, g, b))
                coordinates.append((x, y))
                x += 1
    return colours, coordinates


def alg_rgb(x_max, y_max):
    """
    Iterate through red -> green -> blue
    :param x_max:
    :param y_max:
    """
    x = 0
    y = 0

    colours = []
    coordinates = []
    for colour in helpers.generate_colours(Colour):
        if x >= x_max:
            x = 0
            y += 1
        if y >= y_max:
            y = 0
        colours.append(colour)
        coordinates.append((x, y))
        x += 1

    return colours, coordinates


def alg_bgr(x_max, y_max):
    """
    Iterate through blue -> green -> red
    :param x_max:
    :param y_max:
    """
    x = 0
    y = 0
    colours = []
    coordinates = []

    for b in range(1, 33):
        for g in range(1, 33):
            for r in range(1, 33):
                if x >= x_max:
                    x = 0
                    y += 1
                if y >= y_max:
                    y = 0
                colours.append(Colour(r, g, b))
                coordinates.append((x, y))
                x += 1
    return colours, coordinates


def alg_grb(x_max, y_max):
    """
    Iterate through green -> red -> blue
    :param x_max:
    :param y_max:
    """
    x = 0
    y = 0
    colours = []
    coordinates = []

    for g in range(1, 33):
        for r in range(1, 33):
            for b in range(1, 33):
                if x >= x_max:
                    x = 0
                    y += 1
                if y >= y_max:
                    y = 0
                colours.append(Colour(r, g, b))
                coordinates.append((x, y))
                x += 1
    return colours, coordinates


def alg_rbg(x_max, y_max):
    """
    Iterate through red -> blue -> green
    :param x_max:
    :param y_max:
    """
    x = 0
    y = 0
    colours = []
    coordinates = []

    for r in range(1, 33):
        for b in range(1, 33):
            for g in range(1, 33):
                if x >= x_max:
                    x = 0
                    y += 1
                if y >= y_max:
                    y = 0
                colours.append(Colour(r, g, b))
                coordinates.append((x, y))
                x += 1
    return colours, coordinates


def create_image(algorithm):
    """
    :param algorithm: The name of an algorithm function
    :return:
    """
    canvas = Canvas(256, 128)
    colours, coordinates = eval(algorithm)(canvas.x_size, canvas.y_size)
    canvas.generate_from_list(colours, coordinates)
    return canvas.image
