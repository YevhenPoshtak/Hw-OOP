from math import factorial, log


def sequence_a(x, k):
    for i in range(k + 1):
        yield (x ** (2 * i)) / factorial(2 * i)

def evaluate_a(x, k):
    return (x ** (2 * k)) / factorial(2 * k)

def sequence_b(n):
    p = 1
    for k in range(1, n + 1):
        p *= (1 + 1 / (k ** 2))
        yield p

def evaluate_b(n):
    p = 1
    for k in range(1, n + 1):
        p *= (1 + 1 / (k ** 2))
    return p

def sequence_c(a, b, n):
    if n < 1: return
    d1 = a + b
    yield d1
    if n == 1: return
    d2 = (a + b) ** 2 - a * b
    yield d2
    prev2, prev1 = d1, d2
    for _ in range(3, n + 1):
        curr = (a + b) * prev1 - a * b * prev2
        yield curr
        prev2, prev1 = prev1, curr

def evaluate_c(a, b, n):
    if n < 1: return 0
    if n == 1: return a + b
    d1 = a + b
    d2 = (a + b) ** 2 - a * b
    if n == 2: return d2
    prev2, prev1 = d1, d2
    for _ in range(3, n + 1):
        curr = (a + b) * prev1 - a * b * prev2
        prev2, prev1 = prev1, curr
    return prev1

def sequence_d(n):
    a = [1, 1, 1]
    s = 0
    for k in range(1, n + 1):
        if k > 3: a.append(a[k-2] + a[k-4])
        s += a[k-1] / (2 ** k)
        yield s

def evaluate_d(n):
    a = [1, 1, 1]
    s = 0
    for k in range(1, n + 1):
        if k > 3: a.append(a[k-2] + a[k-4])
        s += a[k-1] / (2 ** k)
    return s

def taylor_series_e(x, eps):
    term = s = x
    n = 0
    yield s
    while abs(term) > eps:
        n += 1
        term *= x * x * (2 * n - 1) / (2 * n + 1)
        s += term
        yield s

def evaluate_e(x, eps):
    if abs(x) >= 1: raise ValueError("|x| має бути < 1")
    term = s = x
    n = 0
    while abs(term) > eps:
        n += 1
        term *= x * x * (2 * n - 1) / (2 * n + 1)
        s += term
    return 2 * s

inputs = [
    ('a', 'input_a.txt', lambda f: (float(f.readline().strip()), int(f.readline().strip())),
     lambda x, k: (evaluate_a(x, k), sequence_a(x, k), f"x_{k}", "Послідовність", lambda i, v: f"x_{i} = {v}", 0)),
    ('b', 'input_b.txt', lambda f: (int(f.readline().strip()),),
     lambda n: (evaluate_b(n), sequence_b(n), f"P_{n}", "Послідовність добутків", lambda i, v: f"P_{i} = {v}", 1)),
    ('c', 'input_c.txt', lambda f: (float(f.readline().strip()), float(f.readline().strip()), int(f.readline().strip())),
     lambda a, b, n: (evaluate_c(a, b, n), sequence_c(a, b, n), f"D_{n}", "Послідовність визначників", lambda i, v: f"D_{i} = {v}", 1)),
    ('d', 'input_d.txt', lambda f: (int(f.readline().strip()),),
     lambda n: (evaluate_d(n), sequence_d(n), f"S_{n}", "Послідовність сум", lambda i, v: f"S_{i} = {v}", 1)),
    ('e', 'input_e.txt', lambda f: (float(f.readline().strip()), float(f.readline().strip())),
     lambda x, eps: (evaluate_e(x, eps), taylor_series_e(x, eps), None, "Послідовність часткових сум", lambda i, v: f"Сума {i}: {2 * v}", 0, lambda x, eps: log((1 + x) / (1 - x))))
]

with open('outputs.txt', 'w', encoding='utf-8') as f:
    for task_id, input_file, read_input, process in inputs:
        f.write(f"===== Вихід для завдання {task_id} =====\n")
        try:
            with open(input_file, 'r') as inp:
                args = read_input(inp)
            result, seq, res_label, seq_label, format_seq, start_idx, *extra = process(*args)
            if task_id == 'e':
                exact = extra[0](*args)
                f.write(f"Ряд Тейлора: {result}\nmath.log: {exact}\nРізниця: {abs(result - exact)}\n")
            elif res_label:
                f.write(f"{res_label} = {result}\n")
            f.write(f"{seq_label}:\n")
            for i, val in enumerate(seq, start_idx):
                f.write(f"{format_seq(i, val)}\n")
        except FileNotFoundError:
            f.write(f"Помилка: {input_file} не знайдено\n")
        f.write("\n")