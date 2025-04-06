import math
class Rational:
    def __init__(self, *args):
        if len(args) == 2:
            n, d = args
            if not isinstance(n, int) or not isinstance(d, int):
                raise TypeError("Чисельник і знаменник повинні бути цілими числами")
            if d == 0:
                raise ZeroDivisionError("Знаменник не може бути нулем")
            self.n = n
            self.d = d
            self._reduce()
        elif len(args) == 1:
            s = args[0]
            if not isinstance(s, str):
                raise TypeError("Один аргумент має бути рядком")
            parts = s.split('/')
            if len(parts) != 2:
                raise ValueError("Неправильний формат раціонального числа")
            n, d = int(parts[0]), int(parts[1])
            if d == 0:
                raise ZeroDivisionError("Знаменник не може бути нулем")
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
            return NotImplemented
        n = self.n * other.d + other.n * self.d
        d = self.d * other.d
        return Rational(n, d)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            return NotImplemented
        n = self.n * other.d - other.n * self.d
        d = self.d * other.d
        return Rational(n, d)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            return NotImplemented
        n = self.n * other.n
        d = self.d * other.d
        return Rational(n, d)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            return NotImplemented
        if other.n == 0:
            raise ZeroDivisionError("Ділення на нуль неможливе")
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
                raise ZeroDivisionError("Знаменник не може бути нулем")
            self.d = value
        self._reduce()

    def __str__(self):
        return f"{self.n}/{self.d}"

    def __repr__(self):
        return f"Rational({self.n}, {self.d})"

precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

def tokenize(expression):
    tokens = []
    for token in expression.split():
        if token in ['+', '-', '*', '/']:
            tokens.append(token)
        elif '/' in token:
            tokens.append(Rational(token))
        else:
            tokens.append(Rational(int(token), 1))
    return tokens

def infix_to_postfix(tokens):
    output = []
    operators = []
    for token in tokens:
        if isinstance(token, Rational):
            output.append(token)
        elif token in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
    while operators:
        output.append(operators.pop())
    return output

def evaluate_postfix(postfix):
    stack = []
    for token in postfix:
        if isinstance(token, Rational):
            stack.append(token)
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
    return stack[0]

with open('input01.txt', 'r') as file:
    expressions = file.readlines()

for expr in expressions:
    expr = expr.strip()
    if expr:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        result = evaluate_postfix(postfix)
        print(f"{expr} = {result}")

