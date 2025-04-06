class Rational:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("Знаменник не може бути нулем")
        self.numerator = numerator
        self.denominator = denominator
        self._normalize()

    def _gcd(self, a, b):
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

    def _normalize(self):
        gcd = self._gcd(self.numerator, self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def __add__(self, other):
        if isinstance(other, int):
            other = Rational(other)
        num = self.numerator * other.denominator + other.numerator * self.denominator
        denom = self.denominator * other.denominator
        return Rational(num, denom)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"


class RationalList:
    def __init__(self):
        self._items = []

    def append(self, item):
        if isinstance(item, Rational):
            self._items.append(item)
        elif isinstance(item, int):
            self._items.append(Rational(item))
        else:
            raise ValueError("Елемент має бути типу Rational або int")

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self._items[index] = value
        elif isinstance(value, int):
            self._items[index] = Rational(value)
        else:
            raise ValueError("Значення має бути типу Rational або int")

    def __len__(self):
        return len(self._items)

    def __add__(self, other):
        result = RationalList()
        result._items = self._items.copy()
        if isinstance(other, RationalList):
            result._items.extend(other._items)
        elif isinstance(other, (Rational, int)):
            result.append(other)
        else:
            raise ValueError("Правий операнд має бути RationalList, Rational або int")
        return result

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            self._items.extend(other._items)
        elif isinstance(other, (Rational, int)):
            self.append(other)
        else:
            raise ValueError("Правий операнд має бути RationalList, Rational або int")
        return self

    def sum(self):
        if not self._items:
            return Rational(0)
        result = self._items[0]
        for item in self._items[1:]:
            result = result + item
        return result

    def __str__(self):
        return "[" + ", ".join(str(item) for item in self._items) + "]"


def parse_rational_string(line):
    rational_list = RationalList()
    numbers = line.strip().split()
    for num in numbers:
        if '/' in num:
            numerator, denominator = map(int, num.split('/'))
            rational_list.append(Rational(numerator, denominator))
        else:
            rational_list.append(Rational(int(num)))
    return rational_list


def process_input_files(filenames, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for filename in filenames:
            rational_list = RationalList()
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    for line in file:
                        line_list = parse_rational_string(line)
                        rational_list += line_list
                total_sum = rational_list.sum()
                output_file.write(f"Файл: {filename}\n")
                output_file.write(f"Сума: {total_sum}\n\n")
            except FileNotFoundError:
                output_file.write(f"Файл {filename} не знайдено\n\n")


input_files = ['input01.txt', 'input02.txt', 'input03.txt']
output_file = 'output.txt'

process_input_files(input_files, output_file)


