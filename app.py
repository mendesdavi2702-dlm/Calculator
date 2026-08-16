import flet as ft
from flet import Colors
from lib.operations import add, subtract, multiply, division, square_root, percentage


bot = (
    {'operator': '⌫', 'fonte': Colors.WHITE, 'fundo': Colors.WHITE_24},
    {'operator': 'AC', 'fonte': Colors.WHITE, 'fundo': Colors.WHITE_24},
    {'operator': '%', 'fonte': Colors.WHITE, 'fundo': Colors.WHITE_24},
    {'operator': '÷', 'fonte': Colors.WHITE, 'fundo': Colors.RED_900},
    {'operator': '7', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '8', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '9', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': 'X', 'fonte': Colors.WHITE, 'fundo': Colors.RED_900},
    {'operator': '4', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '5', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '6', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '-', 'fonte': Colors.WHITE, 'fundo': Colors.RED_900},
    {'operator': '1', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '2', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '3', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '+', 'fonte': Colors.WHITE, 'fundo': Colors.RED_900},
    {'operator': '√', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '0', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': ',', 'fonte': Colors.WHITE, 'fundo': Colors.GREY_900},
    {'operator': '=', 'fonte': Colors.WHITE, 'fundo': Colors.RED_900},
)

def main(page: ft.Page):
    page.bgcolor = "#001"
    page.window.resizable = False
    page.title = "Calculator"
    page.window.width = 280
    page.window.height = 430
    page.window.always_on_top = True

    def update_visor(text):
        visor.value = text
        page.update()

    def format_result(result):
        result = round(result, 8)
        if result == int(result):
            return str(int(result))
        else:
            return str(result).replace(".",",")

    def select(e):
        nonlocal num_current
        nonlocal num_previous
        nonlocal pending_operator
        value_click = e.control.content.value
        #print(f"clicked: '{value_click}' | is digit? {value_click.isdigit()} | num_current before: '{num_current}'")

        if value_click.isdigit():
            if len(num_current) < max_digits:
                num_current = num_current + value_click
                update_visor(num_current)
            #print(f"num_current later: '{num_current}' | visor_value: '{visor.value}'")
        elif value_click == "AC":
            num_current = ""
            update_visor("0")
        elif value_click == "⌫":
            num_current = num_current[:-1]
            if num_current == "":
                update_visor("0")
            else:
                update_visor(num_current)
        elif value_click == "," and "," not in num_current:
            num_current = num_current + value_click
            update_visor(num_current)
        elif value_click in ("+", "-", "X", "÷", "%"):
            num_previous = num_current
            pending_operator = value_click
            num_current = ""
            #print(f"clicked: '{num_previous}' | saved: '{pending_operator}' | number current: '{num_current}'")
        elif value_click == "√":
            try:
                n = float(num_current.replace(",","."))
                result = square_root(n)
                update_visor(format_result(result))
                num_current = format_result(result)
            except ValueError:
                update_visor("ERROR")

        elif value_click == "=":
            try:
                n1 = float(num_previous.replace(",","."))
                n2 = float(num_current.replace(",","."))
                if pending_operator == "+":
                    result = add(n1, n2)
                elif pending_operator ==  "-":
                    result = subtract(n1, n2)
                elif pending_operator == "X":
                    result = multiply(n1, n2)
                elif pending_operator == "÷":
                    result = division(n1, n2)
                elif pending_operator == "%":
                    result = percentage(n1, n2)

                text_result = format_result(result)

                if len(text_result) > max_digits:
                    num_current = text_result[:max_digits - 3] + "..."
                else:
                    num_current = text_result
                update_visor(num_current)

                num_previous = ""
                pending_operator = ""
            except ValueError as error:
                update_visor("ERROR")

    max_digits = 9               
    num_current = ""
    num_previous = ""
    pending_operator = ""

    visor = ft.Text(value="0", color=Colors.WHITE, size=45) 
    display = ft.Row(controls=[visor],
                     alignment=ft.MainAxisAlignment.END)

    buttons = [ft.Container(
        content=ft.Text(value=btn['operator'], color=btn['fonte']),
        width=50,
        height=50,
        bgcolor=btn['fundo'],
        border_radius=100,
        alignment=ft.Alignment.CENTER,
        on_click=select
    )   for btn in bot]

    keyboard = ft.Row(
        width=280,
        wrap=True,
        controls=buttons,
        alignment=ft.MainAxisAlignment.END
    )


    page.add(display, keyboard)


ft.run(main)