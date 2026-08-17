# Calculator — Console + Flet

[🇧🇷 Português](README.md) | 🇺🇸 English

Python calculator project, built in two stages: first a terminal (console) version, then a visual app using the Flet library. Both versions share the same calculation logic, tested with pytest.

This README documents not just the final result, but the process — decisions made, bugs found along the way, and the reasoning behind each change. The idea is that the evolution history is as much a part of the portfolio as the finished code.

## Features

- Operations: addition, subtraction, multiplication, division, square root, percentage
- Calculation history saved to a file (`history.csv`), with date and time
- Error handling for division by zero and square root of a negative number, in both versions
- Visual app (Flet) with:
  - Full number pad, decimal comma, backspace (⌫) and clear (AC)
  - Result formatted in Brazilian number style (comma instead of period, no unnecessary `.0`)
  - Digit limit on screen, with an indicator (`...`) when the result is larger than the available space
  - Grid layout, distinct colors for numbers and operators

## Project structure

```
Calculator/
├── system.py             # console version (terminal)
├── app.py                 # visual version (Flet)
├── lib/
│   ├── operations.py       # pure, tested calculation functions
│   └── history.py           # save and read history from file
├── tests/
│   └── test_operations.py
├── .gitignore
└── README.md
```

## How to run

```bash
python system.py              # console version
python app.py                  # visual version (Flet)
python -m pytest tests/        # runs the 8 automated tests
```

External dependency: `flet` (`pip install flet`). Everything else uses only the Python standard library.

---

## Project evolution

### 1. Starting point: separating logic from interface

Before writing anything, the most important structural decision was: **calculation functions never read input or print anything.**

```python
def add(a: float, b: float) -> float:
    return a + b

def division(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
```

Each function receives numbers and returns a result — no `input()` or `print()` inside them. This choice, made early on, is why it was possible to:
- Automatically test each function with pytest, without needing to simulate keyboard input
- Reuse the exact same functions in both the console and, later, the Flet app, without duplicating logic

### 2. Tests before anything else

Each function has a normal-case test and, where applicable, an error-case test:

```python
def test_division_by_zero():
    with pytest.raises(ValueError):
        division(5, 0)

def test_square_root_negative():
    with pytest.raises(ValueError):
        square_root(-4)
```

Common early mistake: writing `assert add(2 + 2) == 4` instead of `assert add(2, 2) == 4` — resolving the math *before* calling the function, instead of letting the function do the math. Fixed by understanding that `assert` should test with the "raw" numbers, compared against the result already worked out by hand.

### 3. Console (`system.py`)

Simple menu in a loop, with `try/except` on the two operations that can fail:

```python
elif option == 4:
    a = float(input("First number: "))
    b = float(input("Second number: "))
    try:
        result = division(a, b)
        print(f'Result: {result}')
        save_operations('division', result)
    except ValueError as error:
        print(f'ERROR: {error}')
```

History saved as CSV, with formatted date (`datetime.now().strftime(...)`) instead of the full timestamp with microseconds, which was unreadable.

### 4. Removed exponentiation (`power`) from the entire project

While planning the visual app's buttons, it became clear that adding both exponentiation and square root would break the grid layout (5 rows of 4 would turn into an incomplete final row). Decision: keep only square root in the app, and **completely remove** exponentiation — function, test, and menu option — instead of leaving it "forgotten" only in the console. Priority was consistency between the two versions, not full operation coverage.

### 5. Visual app — first obstacles with Flet

Flet changed quite a bit between versions, and a good part of the early work was adapting outdated examples to the installed version (0.86.5):

- `ft.app(target=main)` → `ft.run(main)` (old method deprecated)
- `ElevatedButton(text="1", ...)` → `ElevatedButton(content="1", ...)` (renamed parameter)
- `ElevatedButton` → `Button` (the control itself was deprecated in the installed version)

Main takeaway: instead of relying on outdated tutorials, using `help()` directly on the installed library gave more reliable answers:
```bash
python -c "import flet as ft; help(ft.ElevatedButton.__init__)"
```

### 6. `global` vs `nonlocal`

The calculator's state variables (`num_current`, `num_previous`, `pending_operator`) are created inside `main()`, not at file level. Using `global` inside the click function created a new, disconnected variable instead of updating the existing one — the app "forgot" what had already been typed. Fixed by switching to `nonlocal`, which looks up the variable in the enclosing function's scope (`main`), not at file level.

### 7. Indentation bug: the "=" block always running

At one point, the `"="` calculation block was written as a separate `try`, outside the `if/elif` chain in `select()`, instead of being another `elif`. Result: the calculation block ran on **every** call to `select()`, even when clicking a number — raising `cannot access local variable 'result'` because no inner condition matched. Fixed by restructuring it as `elif value_click == "=":`, at the same level as the other `elif` branches.

### 8. Result formatting

Since every function in `operations.py` returns a `float`, `7 + 2` arrived as `"9.0"` on the display, with a period instead of a comma. `format_result()` solves this in one place:

```python
def format_result(result):
    result = round(result, 8)
    if result == int(result):
        return str(int(result))
    else:
        return str(result).replace(".", ",")
```

Rounding to 8 decimal places also avoids results like `94.44444444444444`, common in divisions, which wouldn't fit on screen.

### 9. Digit limit and the "..."

Initial attempt: a font that shrank dynamically as the number grew. It worked, but the result was visually inconsistent (font size changing with every digit typed). Final decision: **fixed font size**, with a digit limit (`max_digits`) on both typing and the displayed result.

When the calculated result exceeds the limit, instead of silently cutting the text (which would show a wrong number without warning) or hard-failing with a generic error, the app shows however many digits fit, followed by an ellipsis:

```python
if len(text_result) > max_digits:
    num_current = text_result[:max_digits - 3] + "..."
else:
    num_current = text_result
```

This communicates to the user that the value was truncated, without blocking further use of the calculator.

### 10. Copy to clipboard — implemented, then removed

Clipboard support was implemented at one point, using Flet's `Clipboard` service (an async API, using `async/await`):

```python
async def copy_visor(e):
    await clipboard.set(visor.value)
```

It worked, but required wrapping the display in an extra `Container` to capture the click, which misaligned the button grid below it. The feature was removed — in this project, a consistent visual layout took priority over a secondary feature.

### 11. File structure — folders turned into files (and back)

During development, two folder/file mix-ups happened:
- `test_operations.py` was created as a folder instead of a file (containing an `__init__.py` inside)
- `operations.py` and `history.py` were initially written inside the `__init__.py` of an `operations/` folder, instead of as direct files

Both cases technically worked (Python allows logic inside `__init__.py`), but they diverge from what most code reviewers expect. Fixed by moving the content into direct files (`lib/operations.py`, `lib/history.py`) and removing the extra folders.

---

## Tests

8 tests covering the normal case for each operation and the 2 handled error cases (division by zero, square root of a negative number):

```bash
python -m pytest tests/
```

## Possible next steps

- Scientific notation for results exceeding the digit limit, instead of truncating
- Bring exponentiation back, adjusting the layout to fit the extra button
- Copy to clipboard, revisiting the layout so it doesn't misalign the grid
