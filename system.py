from lib.operations import add, subtract, multiply, division, square_root, percentage
from lib.history import save_operations, read_history
from time import sleep

while True:
    print('''
1 - add    
2 - subtract    
3 - multiply    
4 - division
5 - square_root
6 - percentage 
7 - View history
8 - Exit   
''')
    option = int(input("Choose an option: "))

    if option == 1:
        a = float(input("First number: "))
        b = float(input("Second number: "))
        result = add(a, b)
        print(f'Result: {result}')
        save_operations('add', result)
        sleep(2)
    elif option == 2:
        a = float(input("First number: "))
        b = float(input("Second number: "))
        result = subtract(a, b)
        print(f'Result: {result}')
        save_operations('subtract', result)
        sleep(2)
    elif option == 3:
        a = float(input("First number: "))
        b = float(input("Second number: "))
        result = multiply(a, b)
        print(f'Result: {result}')
        save_operations('multiply', result)
        sleep(2)
    elif option == 4:
        a = float(input("First number: "))
        b = float(input("Second number: "))
        try:
            result = division(a, b)
            print(f'Result: {result}')
            save_operations('division', result)
            sleep(2)
        except ValueError as error:
            print(f'ERROR: {error}')
            sleep(2)
    elif option == 5:
        a = float(input("Number: "))
        try:
            result = square_root(a)
            print(f'Result: {result}')
            save_operations('square_root', result)
            sleep(2)
        except ValueError as error:
            print(f'ERROR: {error}')
            sleep(2)
    elif option == 6:
        a = float(input("First number: "))
        b = float(input("Second number: "))
        result = percentage(a, b)
        print(f'Result: {result}')
        save_operations('percentage', result)
        sleep(2)
    elif option == 7:
        try:
            print(read_history())
            sleep(2)
        except FileNotFoundError:
            print("No history yet. Make a calculation first!")
            sleep(2)
    elif option == 8:
        print('Exit ...')
        sleep(2)
        break