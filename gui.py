from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import simpledialog, filedialog
import colours
import helpers


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master


        # Initialise instance variables
        self.algorithms_index = 0
        self.menu = None
        self.regenerate_button = False
        # Produce image and render of it
        self.image = self.generate_image()
        self.render = ImageTk.PhotoImage(self.image)

        self.window_title = "Colour Challenge"
        self.show_algorithm()
        self.init_window()

        # Sets columns to have a weight, so that frames resize when the window is resized.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create canvas widget for image
        self.display = Canvas(self, bd=0, highlightthickness=0)

        # Display the image
        self.display.create_image(0, 0, image=self.render, anchor=NW)
        self.display.grid(row=0, sticky=W+E+N+S)
        self.pack(fill=BOTH, expand=True)

        # When the window is resized, resize the image.
        self.bind("<Configure>", self._window_resize_event)

    def _window_resize_event(self, event):
        self.resize_image(event.width, event.height)

    def resize_image(self, width, height, input_image=None):
        # Fits image to the size of the window
        size = (width, height)
        image = self.image.resize(size, 1)
        if input_image:
            return image
        self.image = image
        self.render = ImageTk.PhotoImage(image)
        self.display.delete()
        self.display.create_image(0, 0, image=self.render, anchor=NW)

    def init_window(self):
        # Generates top menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        menu.add_command(label="Quit", command=self.quit)
        menu.add_command(label="Previous", command=self.previous_image)
        menu.add_command(label="Next", command=self.next_image)
        menu.add_command(label="Open", command=self.open_image)
        menu.add_command(label="Save", command=self.save_image)
        self.menu = menu

    def show_image(self):
        width = self.winfo_width()
        height = self.winfo_height()
        if (width > 1) and (height > 1):
            # Checks that the window has been initialised, and is reporting the correct dimensions.
            self.resize_image(width, height)

        self.display.delete()
        self.display.create_image(0, 0, image=self.render, anchor=NW)

    def generate_image(self):
        # Generate an image using the colours module
        image = colours.create_image(algorithms[self.algorithms_index])
        render = ImageTk.PhotoImage(image)
        self.image = image
        self.render = render
        return image

    def show_algorithm(self):
        algorithm = algorithms[self.algorithms_index]
        algorithm = algorithm.replace("alg_", "")
        parts = algorithm.split("_")
        algorithm = ' '.join([part.capitalize() for part in parts])
        if (len(algorithm) == 3) and (all(component in algorithm.lower() for component in ['r', 'g', 'b'])):
            algorithm = algorithm.upper()
        self.master.title("{} - {}".format(self.window_title, algorithm))

    def toggle_regenerate_button(self, enable=False):
        label = "Regenerate"
        if enable and (not self.regenerate_button):
            self.menu.add_command(label=label, command=self.regenerate_image)
            self.regenerate_button = True

        elif (not enable) and self.regenerate_button:
            self.menu.delete(label)
            self.regenerate_button = False

    def regenerate_image(self):
        self.generate_image()
        self.show_image()

    def previous_image(self):
        if self.algorithms_index == 0:
            self.algorithms_index = len(algorithms) - 1
        else:
            self.algorithms_index -= 1
        self.regenerate_image()
        if "random" in algorithms[self.algorithms_index]:
            self.toggle_regenerate_button(enable=True)
        else:
            self.toggle_regenerate_button(enable=False)
        self.show_algorithm()

    def next_image(self):
        if self.algorithms_index == len(algorithms) - 1:
            self.algorithms_index = 0
        else:
            self.algorithms_index += 1
        self.regenerate_image()
        if "random" in algorithms[self.algorithms_index]:
            self.toggle_regenerate_button(enable=True)
        else:
            self.toggle_regenerate_button(enable=False)
        self.show_algorithm()

    def save_image(self):
        # Create a save as dialog
        dimensions = simpledialog.askstring("Dimensions", "Save image with dimensions (width, height)")
        width, height = [int(dimension) for dimension in dimensions.split(", ")]
        image = self.resize_image(width, height, input_image=self.image)

        path = filedialog.asksaveasfile(mode='w', defaultextension='.png')
        if not path:
            return
        try:
            image.save(path.name)
        except IOError:
            simpledialog.messagebox.showinfo("Save", "Failed to save to  {}.".format(path.name))
            return

    def open_image(self):
        # Create an open file dialog
        path = filedialog.askopenfile()
        if not path:
            return
        try:
            self.image = PIL.Image.open(path.name)
        except (KeyError, IOError):
            simpledialog.messagebox.showinfo("Open", "Failed to open {}.".format(path.name))
            return
        self.render = ImageTk.PhotoImage(self.image)
        self.show_image()
        self.master.title(self.window_title)
        return self.image

    def quit(self):
        exit()


algorithms = helpers.generate_algorithms()

root = Tk()
root.geometry("1000x600")
app = Window(root)
root.mainloop()
