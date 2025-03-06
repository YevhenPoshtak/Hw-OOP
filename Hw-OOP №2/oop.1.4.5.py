import math

class Matrix2D:
    def __init__(self):
        self.data = [[0, 0], [0, 0]]

    def input_from_keyboard(self):
        print("Enter 4 elements of 2x2 matrix:")
        for i in range(2):
            row = input(f"Row {i+1}: ").split()
            self.data[i] = [float(x) for x in row]

    def input_from_file(self, file):
        line = file.readline().strip().split()
        if len(line) == 4:
            self.data[0] = [float(line[0]), float(line[1])]
            self.data[1] = [float(line[2]), float(line[3])]

    def print_to_screen(self):
        for row in self.data:
            print(" ".join(map(str, row)))

    def print_to_file(self, file):
        for row in self.data:
            file.write(" ".join(map(str, row)) + "\n")

    def determinant(self):
        return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

    def is_degenerate(self):
        return abs(self.determinant()) < 1e-10

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def input_from_file(self, file):
        line = file.readline().strip().split()
        if len(line) == 2:
            self.x = float(line[0])
            self.y = float(line[1])

    def print_to_file(self, file):
        file.write(f"x = {self.x}, y = {self.y}\n")

class Solver:
    def __init__(self, matrix, vector):
        self.A = matrix
        self.b = vector

    def solve_cramer(self):
        detA = self.A.determinant()
        if self.A.is_degenerate():
            return Vector2D(math.nan, math.nan)
        Ax = Matrix2D()
        Ax.data = [[self.b.x, self.A.data[0][1]], [self.b.y, self.A.data[1][1]]]
        detX = Ax.determinant()

        Ay = Matrix2D()
        Ay.data = [[self.A.data[0][0], self.b.x], [self.A.data[1][0], self.b.y]]
        detY = Ay.determinant()

        return Vector2D(detX / detA, detY / detA)

def main():
    try:
        with open("matrix_coefficients.txt", "r") as matrix_file, \
             open("rhs_values.txt", "r") as rhs_file, \
             open("output.txt", "w") as output_file:

            matrices = []
            rhs_vectors = []

            while True:
                m = Matrix2D()
                m.input_from_file(matrix_file)
                if not matrix_file.tell() == matrix_file.seek(0, 2):  # Перевірка кінця файлу
                    matrices.append(m)
                else:
                    break

            while True:
                v = Vector2D()
                v.input_from_file(rhs_file)
                if not rhs_file.tell() == rhs_file.seek(0, 2):
                    rhs_vectors.append(v)
                else:
                    break

            if len(matrices) != len(rhs_vectors):
                print("Mismatch between number of matrices and RHS vectors!")
                return

            output_file.write(f"Solutions for {len(matrices)} systems:\n")
            for i, (matrix, rhs) in enumerate(zip(matrices, rhs_vectors), 1):
                output_file.write(f"\nSystem {i}:\nMatrix:\n")
                matrix.print_to_file(output_file)
                output_file.write(f"RHS: {rhs.x} {rhs.y}\n")

                solver = Solver(matrix, rhs)
                solution = solver.solve_cramer()

                output_file.write("Solution: ")
                if math.isnan(solution.x):
                    output_file.write("No unique solution (degenerate system)\n")
                else:
                    solution.print_to_file(output_file)

        print("Results written to output.txt")

    except FileNotFoundError:
        print("Error: One of the input files not found!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()