import math

class RationalError(ZeroDivisionError):
    def __init__(self, message="Знаменник не може бути нулем"):
        self.message = message
        super().__init__(self.message)

class RationalValueError(ValueError):
    def __init__(self, message="Некоректні дані для операцій з раціональними числами"):
        self.message = message
        super().__init__(self.message)

class Rational:
    def __init__(self, *args):
        if len(args) == 2:
            n, d = args
            if not isinstance(n, int) or not isinstance(d, int):
                raise TypeError("Чисельник і знаменник повинні бути цілими числами")
            if d == 0:
                raise RationalError("Знаменник не може бути нулем")
            self.n = n
            self.d = d
            self._reduce()
        elif len(args) == 1:
            s = args[0]
            if isinstance(s, int):
                self.n = s
                self.d = 1
                return
            if not isinstance(s, str):
                raise TypeError("Один аргумент має бути рядком або цілим числом")
            parts = s.split('/')
            if len(parts) != 2:
                raise ValueError("Неправильний формат раціонального числа")
            try:
                n, d = int(parts[0]), int(parts[1])
            except ValueError:
                raise RationalValueError("Некоректний формат чисел у рядку")
            if d == 0:
                raise RationalError("Знаменник не може бути нулем")
            self.n = n
            self.d = d
            self._reduce()
        else:
            raise TypeError("Неправильна кількість аргументів")

    def _reduce(self):
        gcd = math.gcd(self.n, self.d)
        self.n //= gcd
        self.d //= gcd
        if self.d < 0:
            self.n = -self.n
            self.d = -self.d

    def __add__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            raise RationalValueError("Додавання можливе лише з Rational або int")
        n = self.n * other.d + other.n * self.d
        d = self.d * other.d
        return Rational(n, d)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            raise RationalValueError("Віднімання можливе лише з Rational або int")
        n = self.n * other.d - other.n * self.d
        d = self.d * other.d
        return Rational(n, d)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            raise RationalValueError("Множення можливе лише з Rational або int")
        n = self.n * other.n
        d = self.d * other.d
        return Rational(n, d)

    def __truediv__(self, other):
        if isinstance(other, int):
            if other == 0:
                raise RationalError("Ділення на нуль неможливе")
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            raise RationalValueError("Ділення можливе лише з Rational або int")
        if other.n == 0:
            raise RationalError("Ділення на нуль неможливе")
        n = self.n * other.d
        d = self.d * other.n
        return Rational(n, d)

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == "n":
            return self.n
        elif key == "d":
            return self.d
        else:
            raise KeyError("Неправильний ключ")

    def __setitem__(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Значення має бути цілим числом")
        if key == "n":
            self.n = value
        elif key == "d":
            if value == 0:
                raise RationalError("Знаменник не може бути нулем")
            self.d = value
        else:
            raise KeyError("Неправильний ключ")
        self._reduce()

    def __str__(self):
        return f"{self.n}/{self.d}"

    def __repr__(self):
        return f"Rational({self.n}, {self.d})"

class RationalList:
    def __init__(self):
        self._items = []

    def append(self, item):
        if isinstance(item, Rational):
            self._items.append(item)
        elif isinstance(item, int):
            self._items.append(Rational(item, 1))
        elif isinstance(item, str):
            try:
                self._items.append(Rational(item))
            except (RationalError, RationalValueError, ValueError, TypeError) as e:
                raise RationalValueError(f"Неможливо додати '{item}': {str(e)}")
        else:
            raise RationalValueError(f"Елемент має бути типу Rational, int або коректним рядком, отримано {type(item).__name__}")

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self._items[index] = value
        elif isinstance(value, int):
            self._items[index] = Rational(value, 1)
        elif isinstance(value, str):
            try:
                self._items[index] = Rational(value)
            except (RationalError, RationalValueError, ValueError, TypeError) as e:
                raise RationalValueError(f"Неможливо встановити '{value}': {str(e)}")
        else:
            raise RationalValueError(f"Значення має бути типу Rational, int або коректним рядком, отримано {type(value).__name__}")

    def __len__(self):
        return len(self._items)

    def __add__(self, other):
        result = RationalList()
        result._items = self._items.copy()
        if isinstance(other, RationalList):
            result._items.extend(other._items)
        elif isinstance(other, (Rational, int)):
            result.append(other)
        elif isinstance(other, str):
            try:
                result.append(Rational(other))
            except (RationalError, RationalValueError, ValueError, TypeError) as e:
                raise RationalValueError(f"Неможливо додати '{other}': {str(e)}")
        else:
            raise RationalValueError(f"Правий операнд має бути RationalList, Rational, int або коректним рядком, отримано {type(other).__name__}")
        return result

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            self._items.extend(other._items)
        elif isinstance(other, (Rational, int)):
            self.append(other)
        elif isinstance(other, str):
            try:
                self.append(Rational(other))
            except (RationalError, RationalValueError, ValueError, TypeError) as e:
                raise RationalValueError(f"Неможливо додати '{other}': {str(e)}")
        else:
            raise RationalValueError(f"Правий операнд має бути RationalList, Rational, int або коректним рядком, отримано {type(other).__name__}")
        return self

    def sum(self):
        if not self._items:
            return Rational(0, 1)
        result = self._items[0]
        for item in self._items[1:]:
            result = result + item
        return result

    def __str__(self):
        return "[" + ", ".join(str(item) for item in self._items) + "]"

def parse_rational_string(line, output_file):
    rational_list = RationalList()
    numbers = line.strip().split()
    for num in numbers:
        try:
            if '/' in num:
                parts = num.split('/')
                if len(parts) != 2:
                    raise RationalValueError(f"Неправильний формат раціонального числа: {num}")
                try:
                    numerator, denominator = map(int, parts)
                except ValueError:
                    raise RationalValueError(f"Некоректні числові значення в {num}")
                rational_list.append(Rational(numerator, denominator))
            else:
                try:
                    rational_list.append(int(num))
                except ValueError:
                    raise RationalValueError(f"Некоректне ціле число: {num}")
        except (RationalError, RationalValueError) as e:
            print(f"Помилка при обробці '{num}': {str(e)}", file=output_file)
            continue
    return rational_list

def process_input_files(filenames):
    with open('outputs.txt', 'w', encoding='utf-8') as output_file:
        for filename in filenames:
            print(f"Файл: {filename}", file=output_file)
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(f"Вміст файлу: {content.strip()}", file=output_file)
                    rational_list = parse_rational_string(content, output_file)
                    print(f"Створений RationalList: {rational_list}", file=output_file)
                    print(f"Сума елементів: {rational_list.sum()}", file=output_file)
            except FileNotFoundError:
                print(f"Помилка: Файл {filename} не знайдено", file=output_file)
            except Exception as e:
                print(f"Помилка при обробці файлу {filename}: {str(e)}", file=output_file)

input_files = ['input.1.txt', 'input.2.txt', 'input.3.txt']
process_input_files(input_files)