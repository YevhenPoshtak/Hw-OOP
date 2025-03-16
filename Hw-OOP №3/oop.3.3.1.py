import math
import os


class Figure:
    def dimension(self):
        raise NotImplementedError("Subclass must implement dimension()")
    def perimeter(self):
        return None
    def square(self):
        return None
    def squareSurface(self):
        return None
    def squareBase(self):
        return None
    def height(self):
        return None
    def volume(self):
        if self.dimension() == 2:
            return self.square()
        else:
            raise NotImplementedError("Subclass must implement volume() for 3D figures")


class Triangle(Figure):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def dimension(self):
        return 2
    def perimeter(self):
        return self.a + self.b + self.c
    def square(self):
        if not self.is_valid_triangle():
            return 0
        s = self.perimeter() / 2
        try:
            return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        except ValueError:
            return 0
    def is_valid_triangle(self):
        return (self.a + self.b > self.c and
                self.a + self.c > self.b and
                self.b + self.c > self.a)


class TriangularPyramid(Triangle):
    def __init__(self, base_side, height):
        super().__init__(base_side, base_side, base_side)
        self.pyramid_height = height
    def dimension(self):
        return 3
    def squareSurface(self):
        apothem = (self.a * math.sqrt(3)) / 6
        slant_height = math.sqrt(self.pyramid_height ** 2 + apothem ** 2)
        return 3 * (0.5 * self.a * slant_height)
    def squareBase(self):
        return super().square()
    def height(self):
        return self.pyramid_height
    def volume(self):
        base_area = super().square()
        return (base_area * self.pyramid_height) / 3


class Rectangle(Figure):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def dimension(self):
        return 2
    def perimeter(self):
        return 2 * (self.a + self.b)
    def square(self):
        return self.a * self.b


class QuadrangularPyramid(Rectangle):
    def __init__(self, a, b, height):
        super().__init__(a, b)
        self.pyramid_height = height
    def dimension(self):
        return 3
    def squareSurface(self):
        a, b, h = self.a, self.b, self.pyramid_height
        slant1 = math.sqrt(h ** 2 + (b / 2) ** 2)
        slant2 = math.sqrt(h ** 2 + (a / 2) ** 2)
        return a * slant1 + b * slant2
    def squareBase(self):
        return super().square()
    def height(self):
        return self.pyramid_height
    def volume(self):
        base_area = super().square()
        return (base_area * self.pyramid_height) / 3


class RectangularParallelepiped(Rectangle):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.c = c
    def dimension(self):
        return 3
    def squareSurface(self):
        return 2 * (self.a * self.c + self.b * self.c)
    def squareBase(self):
        return super().square()
    def height(self):
        return self.c
    def volume(self):
        return self.a * self.b * self.c


class Trapeze(Figure):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def dimension(self):
        return 2
    def perimeter(self):
        return self.a + self.b + self.c + self.d
    def square(self):
        a, b, c, d = self.a, self.b, self.c, self.d
        if a < b:
            a, b = b, a
            c, d = d, c
        delta = a - b
        if delta == 0:
            return (a + b) / 2 * c
        numerator = delta ** 2 - c ** 2 + d ** 2
        denominator = 2 * delta
        if denominator == 0:
            return 0
        y = numerator / denominator
        try:
            h = math.sqrt(d ** 2 - y ** 2)
        except ValueError:
            return 0
        return (a + b) / 2 * h


class Parallelogram(Figure):
    def __init__(self, a, b, height):
        self.a = a
        self.b = b
        self.para_height = height
    def dimension(self):
        return 2
    def perimeter(self):
        return 2 * (self.a + self.b)
    def square(self):
        return self.a * self.para_height


class Circle(Figure):
    def __init__(self, radius):
        self.radius = radius
    def dimension(self):
        return 2
    def perimeter(self):
        return 2 * math.pi * self.radius
    def square(self):
        return math.pi * self.radius ** 2


class Ball(Circle):
    def __init__(self, radius):
        super().__init__(radius)
    def dimension(self):
        return 3
    def squareSurface(self):
        return 4 * super().square()
    def volume(self):
        return (4 / 3) * math.pi * self.radius ** 3


class Cone(Circle):
    def __init__(self, radius, height):
        super().__init__(radius)
        self.cone_height = height
    def dimension(self):
        return 3
    def squareSurface(self):
        slant = math.sqrt(self.radius ** 2 + self.cone_height ** 2)
        return math.pi * self.radius * slant
    def squareBase(self):
        return super().square()
    def height(self):
        return self.cone_height
    def volume(self):
        return (super().square() * self.cone_height) / 3


class TriangularPrism(Triangle):
    def __init__(self, a, b, c, height):
        super().__init__(a, b, c)
        self.prism_height = height
    def dimension(self):
        return 3
    def squareSurface(self):
        return super().perimeter() * self.prism_height
    def squareBase(self):
        return super().square()
    def height(self):
        return self.prism_height
    def volume(self):
        base_area = super().square()
        return base_area * self.prism_height


def read_figures(filename):
    figures = []
    figure_info = {
        'Triangle': (Triangle, 3),
        'Rectangle': (Rectangle, 2),
        'Trapeze': (Trapeze, 4),
        'Parallelogram': (Parallelogram, 3),
        'Circle': (Circle, 1),
        'Ball': (Ball, 1),
        'TriangularPyramid': (TriangularPyramid, 2),
        'QuadrangularPyramid': (QuadrangularPyramid, 3),
        'RectangularParallelepiped': (RectangularParallelepiped, 3),
        'Cone': (Cone, 2),
        'TriangularPrism': (TriangularPrism, 4),
    }
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if not parts:
                    continue
                name = parts[0]
                params = parts[1:]
                info = figure_info.get(name)
                if not info:
                    print(f"Unknown figure: {name} in file {filename}")
                    continue
                cls, param_count = info
                if len(params) != param_count:
                    print(f"Invalid number of parameters for {name} in file {filename}")
                    continue
                try:
                    params = list(map(float, params))
                    params = [int(p) if p.is_integer() else p for p in params]
                    instance = cls(*params)
                    figures.append(instance)
                except Exception as e:
                    print(f"Error creating {name} from file {filename}: {e}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return figures


def process_files(files, output_file="output.txt"):
    with open(output_file, 'w') as f:
        f.write("Class Hierarchy (UML):\n")
        f.write("Figure\n")
        f.write("  --> Triangle\n")
        f.write("  |     --> TriangularPyramid\n")
        f.write("  |     --> TriangularPrism\n")
        f.write("  --> Rectangle\n")
        f.write("  |     --> QuadrangularPyramid\n")
        f.write("  |     --> RectangularParallelepiped\n")
        f.write("  --> Trapeze\n")
        f.write("  --> Parallelogram\n")
        f.write("  --> Circle\n")
        f.write("        --> Ball\n")
        f.write("        --> Cone\n")
        f.write("\n")

        for file in files:
            if not os.path.exists(file):
                f.write(f"File {file} does not exist.\n")
                continue
            figures = read_figures(file)
            if not figures:
                f.write(f"No valid figures found in {file}.\n")
                continue
            max_figure = find_max_figure(figures)
            if max_figure:
                f.write(f"\nFigure with the largest measure in {file}:\n")
                write_figure_info(max_figure, f)


def find_max_figure(figures):
    if not figures:
        return None
    return max(figures, key=lambda x: x.volume())


def write_figure_info(figure, file_handle):
    if figure is None:
        return
    file_handle.write(f"Figure: {figure.__class__.__name__}\n")
    if figure.dimension() == 2:
        file_handle.write(f"Perimeter: {figure.perimeter()}\n")
        file_handle.write(f"Area: {figure.square()}\n")
    else:
        file_handle.write(f"Surface Area: {figure.squareSurface()}\n")
        file_handle.write(f"Base Area: {figure.squareBase()}\n")
        file_handle.write(f"Height: {figure.height()}\n")
        file_handle.write(f"Volume: {figure.volume()}\n")


def main():
    files = ['input01.txt', 'input02.txt', 'input03.txt']
    process_files(files)

if __name__ == "__main__":
    main()