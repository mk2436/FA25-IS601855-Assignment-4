"""
Unit tests for the operations module using pytest.

This test suite covers positive, negative, and edge scenarios for the Operation
class's static methods. It ensures arithmetic operations perform correctly,
handles floating-point edge cases, overflow/underflow, division by zero,
and invalid input types.

All tests are fully parameterized for clarity and maintainability.
"""

import math
import pytest
from app.operation import Operation


# -----------------------------------------------------------------------------------
# Addition Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected, comparison",
    [
        (10.0, 5.0, 15.0, "equal"),        # positive + positive
        (-10.0, -5.0, -15.0, "equal"),     # negative + negative
        (10.0, -5.0, 5.0, "equal"),        # positive + negative
        (10.0, 0.0, 10.0, "equal"),        # adding zero
        (0.1, 0.2, 0.3, "approx"),         # floating-point precision check
    ],
)
def test_addition(a, b, expected, comparison):
    result = Operation.addition(a, b)
    if comparison == "approx":
        # Use math.isclose to handle floating-point rounding errors
        assert math.isclose(result, expected, rel_tol=1e-9)
    else:
        assert result == expected


# -----------------------------------------------------------------------------------
# Subtraction Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 5.0, 5.0),       # positive - positive
        (-10.0, -5.0, -5.0),    # negative - negative
        (10.0, -5.0, 15.0),     # positive - negative
        (10.0, 0.0, 10.0),      # subtracting zero
    ],
)
def test_subtraction(a, b, expected):
    result = Operation.subtraction(a, b)
    assert result == expected


# -----------------------------------------------------------------------------------
# Multiplication Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 5.0, 50.0),               # positive * positive
        (-10.0, -5.0, 50.0),             # negative * negative
        (10.0, -5.0, -50.0),             # positive * negative
        (10.0, 0.0, 0.0),                # multiplying by zero
        (1e308, 10.0, float("inf")),     # overflow scenario
    ],
)
def test_multiplication(a, b, expected):
    result = Operation.multiplication(a, b)
    assert result == expected


# -----------------------------------------------------------------------------------
# Division Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 5.0, 2.0),                    # simple division
        (-10.0, -5.0, 2.0),                  # negative / negative
        (10.0, -5.0, -2.0),                  # positive / negative
        (0.0, 5.0, 0.0),                     # zero numerator
        (1e-308, 1e308, 0.0),                # underflow scenario
        (1.0, float("inf"), 0.0),            # finite / infinity
        (float("inf"), 1.0, float("inf")),   # infinity / finite
        (-float("inf"), 1.0, -float("inf")), # negative infinity / finite
    ],
)
def test_division(a, b, expected):
    result = Operation.division(a, b)
    assert result == expected


# Parameterized division by zero test
@pytest.mark.parametrize(
    "a, b",
    [
        (10.0, 0.0),     # positive numerator / zero
        (-5.0, 0.0),     # negative numerator / zero
        (0.0, 0.0),      # zero / zero
    ],
)
def test_division_by_zero(a, b):
    with pytest.raises(ValueError) as exc_info:
        Operation.division(a, b)
    assert str(exc_info.value) == "Division by zero is not allowed."


# -----------------------------------------------------------------------------------
# Power Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "base, exponent, expected",
    [
        (2.0, 3.0, 8.0),          # positive base, positive exponent
        (5.0, 0.0, 1.0),          # any number to the power of zero
        (0.0, 5.0, 0.0),          # zero base, positive exponent
        (0.0, 0.0, 1.0),          # zero base, zero exponent (Python convention)
        (2.0, -3.0, 0.125),       # positive base, negative exponent
        (-2.0, 3.0, -8.0),        # negative base, odd exponent
        (-2.0, 4.0, 16.0),        # negative base, even exponent
    ],
)
def test_power(base, exponent, expected):
    result = Operation.power(base, exponent)
    assert result == expected


# -----------------------------------------------------------------------------------
# Invalid Input Types Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "calc_method, a, b, expected_exception",
    [
        (Operation.addition, '10', 5.0, TypeError),        # string + number
        (Operation.subtraction, 10.0, '5', TypeError),    # number - string
        (Operation.multiplication, '10', '5', TypeError), # string * string
        (Operation.division, 10.0, '5', TypeError),       # number / string
        (Operation.power, '2', 3.0, TypeError),          # string ** number
    ],
)
def test_operations_invalid_input_types(calc_method, a, b, expected_exception):
    with pytest.raises(expected_exception):
        calc_method(a, b)
