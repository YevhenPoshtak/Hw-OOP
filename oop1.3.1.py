import math


class Shape:
    def perimeter(self):
        return 0
    def area(self):
        return 0
    def name(self):
        return ""


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def is_valid(self):
        return (self.a > 0 and self.b > 0 and self.c > 0 and self.a + self.b > self.c and self.b + self.c > self.a and self.a + self.c > self.b)
    def perimeter(self):
        return self.a + self.b + self.c
    def area(self):
        if not self.is_valid():
            return 0
        s = self.perimeter() / 2
        value = s * (s - self.a) * (s - self.b) * (s - self.c)
        return math.sqrt(value) if value > 0 else 0
    def name(self):
        return "Triangle"


class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def is_valid(self):
        return self.a > 0 and self.b > 0
    def perimeter(self):
        return 2 * (self.a + self.b)
    def area(self):
        return self.a * self.b if self.is_valid() else 0
    def name(self):
        return "Rectangle"


class Trapeze(Shape):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def is_valid(self):
        return (self.a >= 0 and self.b >= 0 and self.c > 0 and self.d > 0 and self.c ** 2 > (abs(self.a - self.b) / 2) ** 2)
    def perimeter(self):
        return self.a + self.b + self.c + self.d
    def area(self):
        if not self.is_valid():
            return 0
        h = math.sqrt(self.c ** 2 - (abs(self.a - self.b) / 2) ** 2)
        return (self.a + self.b) / 2 * h
    def name(self):
        return "Trapeze"


class Parallelogram(Shape):
    def __init__(self, a, b, h):
        self.a = a
        self.b = b
        self.h = h
    def is_valid(self):
        return self.a > 0 and self.b > 0 and self.h > 0
    def perimeter(self):
        return 2 * (self.a + self.b)
    def area(self):
        return self.a * self.h if self.is_valid() else 0
    def name(self):
        return "Parallelogram"


class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def is_valid(self):
        return self.r > 0
    def perimeter(self):
        return 2 * math.pi * self.r
    def area(self):
        return math.pi * self.r ** 2 if self.is_valid() else 0
    def name(self):
        return "Circle"


def create_shape(line):
    parts = line.split()
    shape_type = parts[0]
    params = list(map(float, parts[1:]))
    try:
        if shape_type == "Triangle":
            shape = Triangle(*params)
        elif shape_type == "Rectangle":
            shape = Rectangle(*params)
        elif shape_type == "Trapeze":
            shape = Trapeze(*params)
        elif shape_type == "Parallelogram":
            shape = Parallelogram(*params)
        elif shape_type == "Circle":
            shape = Circle(*params)
        else:
            return None
        return shape if shape.is_valid() else None
    except:
        return None


def process_file(filename):
    shapes = []
    try:
        with open(filename, "r") as file:
            for line in file:
                shape = create_shape(line.strip())
                if shape:
                    shapes.append(shape)
    except FileNotFoundError:
        return f"Файл {filename} не знайдено\n", None
    if not shapes:
        return f"Фігури не знайдені у файлі {filename}\n", None
    max_area = max(shapes, key=lambda s: s.area()).area()
    max_perimeter = max(shapes, key=lambda s: s.perimeter()).perimeter()
    for shape in shapes:
        if shape.area() == max_area and shape.perimeter() == max_perimeter:
            return (f"Для файлу {filename}:\n" f"Фігура з найбільшою площею та периметром: {shape.name()} з площею {shape.area():.2f} і периметром {shape.perimeter():.2f}\n"), shape
    return f"Для файлу {filename}: Жодна фігура не має одночасно максимальну площу і периметр\n", None


def main():
    input_files = ["input01.txt", "input02.txt", "input03.txt"]
    output_lines = []
    for filename in input_files:
        message, result = process_file(filename)
        output_lines.append(message)
        if result:
            print(message.strip())
    with open("output.txt", "w", encoding="utf-8") as output_file:
        output_file.writelines(output_lines)


if __name__ == "__main__":
    main()
