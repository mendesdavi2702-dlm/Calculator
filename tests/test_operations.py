from lib.operations import add, division, percentage, square_root, subtract, multiply
import pytest

def test_add():
    assert add(2, 2) == 4

def test_subtract():
    assert subtract(4, 2) == 2

def test_division():
    assert division(6, 2) == 3

def test_percentage():
    assert percentage(200, 15) == 30

def test_square_root():
    assert square_root(9) == 3

def test_multiply():
    assert multiply(5, 5) == 25

def test_division_zero():
    with pytest.raises(ValueError):
        division(5, 0)

def test_square_root_negative():
    with pytest.raises(ValueError):
        square_root(-8)
