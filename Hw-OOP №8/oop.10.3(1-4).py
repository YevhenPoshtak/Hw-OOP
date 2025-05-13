from copy import copy
from random import randint


def isIterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def get_iterable_content(obj):
    if isIterable(obj):
        return " ".join(str(item) for item in obj)
    return ""


def print_function_name(func):
    def wrapper(*args, **kwargs):
        msg = f"Calling function: {func.__name__}"
        print(msg)
        if 'output_messages' in globals():
            output_messages.append(msg)
        return func(*args, **kwargs)

    return wrapper


def print_class_name(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        msg = f"Creating instance of {cls.__name__}"
        print(msg)
        if 'output_messages' in globals():
            output_messages.append(msg)
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


class ProtectedDictInt:
    def __init__(self):
        self.__dict = {}

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise KeyError
        if key in self.__dict:
            raise PermissionError
        self.__dict[key] = value

    def __getitem__(self, key):
        return self.__dict[key]

    def __add__(self, other):
        result_dict = ProtectedDictInt()
        for key, val in self.__dict.items():
            result_dict[key] = val
        if isinstance(other, ProtectedDictInt):
            for key, val in other.__dict.items():
                result_dict[key] = val
        elif isinstance(other, tuple) and len(other) == 2:
            result_dict[other[0]] = other[1]
        else:
            raise ValueError
        return result_dict

    def __sub__(self, other):
        if isinstance(other, int) and other in self:
            result_dict = ProtectedDictInt()
            for key, val in self.__dict.items():
                if key != other:
                    result_dict[key] = val
            return result_dict
        else:
            raise ValueError

    def __contains__(self, key):
        return key in self.__dict

    def __len__(self):
        return len(self.__dict)

    def __str__(self):
        return str(self.__dict)

    def __iter__(self):
        return ProtectedDictIntIterator(self.__dict)


class ProtectedDictIntIterator:
    def __init__(self, collection):
        self._sorted_keys = copy(sorted(list(collection)))
        self._cursor = 0

    def __next__(self):
        try:
            key = self._sorted_keys[self._cursor]
            self._cursor += 1
            return key
        except IndexError:
            raise StopIteration


def construct():
    object_list = []
    d = ProtectedDictInt()
    for i in range(20):
        try:
            key = randint(0, 1000)
            d[key] = key
        except:
            pass
    object_list.append(d)
    object_list.append(10)
    object_list.append("1234")
    object_list.append([1, 3, 4])
    object_list.append(ProtectedDictIntIterator([1, 3]))
    object_list.append(5.3)
    object_list.append({5: 5, 23: 23, 12: 12})
    return object_list


MyClass = type('MyClass', (), {})


@print_function_name
def test_function():
    msg = "Функція виконується"
    print(msg)
    if 'output_messages' in globals():
        output_messages.append(msg)


@print_class_name
class ExampleClass:
    pass


if __name__ == "__main__":
    output_messages = []

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("Завдання 10.3.1:\n")
        lst = construct()
        for obj in lst:
            if isIterable(obj):
                result = f"Об'єкт {obj} підтримує ітераційний протокол. Вміст:\n"
                content = " ".join(str(it) for it in obj)
                result += f"{content}\n"
                f.write(result)
                print(result, end="")

        result = "\nЗавдання 10.3.2:\n"
        obj = MyClass()
        result += f"Створено об'єкт класу {MyClass.__name__}: {obj}\n"
        f.write(result)
        print(result, end="")

        result = "\nЗавдання 10.3.3:\n"
        f.write(result)
        print(result, end="")
        test_function()

        for msg in output_messages:
            f.write(msg + "\n")

        result = "\nЗавдання 10.3.4:\n"
        f.write(result)
        print(result, end="")
        example = ExampleClass()

        for msg in output_messages:
            if "Creating instance" in msg:
                f.write(msg + "\n")