import math

def add(a: float, b: float) -> float:
    return a + b

def division(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def square_root(number: float) -> float:
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return math.sqrt(number)

def percentage(value: float, percent: float) -> float:
    return (value * percent) / 100