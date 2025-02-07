def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    num1 = int(input("Введіть перше число: "))
    num2 = int(input("Введіть друге число: "))
    
    print(f"Найбільший спільний дільник: {gcd(num1, num2)}")
