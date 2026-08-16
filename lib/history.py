import os
from datetime import datetime

arq = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.csv')

def save_operations(operations: str, result: float):
    with open(arq, 'at') as a:
        a.write(f'{datetime.now().strftime("%d/%m/%y %H:%M")};{operations};{result}\n')

def read_history():
    with open(arq, 'rt') as a:
        line = a.readlines()

    formatted_history = ''
    for item in line:
        parts = item.split(';')
        formatted_history += f'{parts[0]} | {parts[1]} | {parts[2]}'

    return formatted_history

