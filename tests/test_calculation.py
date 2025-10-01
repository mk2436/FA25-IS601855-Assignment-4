# tests/test_calculations.py

"""
Fully parameterized unit tests for the calculator_calculations module using pytest.

This test suite covers:
- Positive and negative execution scenarios of calculation classes
- Division by zero and edge cases (large/small/negative numbers)
- Factory instance creation and errors
- String (__str__) and repr (__repr__) formatting

All tests follow the AAA (Arrange, Act, Assert) pattern and PEP8 standards.
"""

import pytest
from unittest.mock import patch
from app.operation import Operation
from app.calculation import (
    CalculationFactory,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
    Calculation
)


# -----------------------------------------------------------------------------------
# Parameterized Positive Execution Tests for Calculation Classes
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, a, b, expected, mock_method",
    [
        (AddCalculation, 10.0, 5.0, 15.0, 'addition'),
        (AddCalculation, -10.0, 5.0, -5.0, 'addition'),
        (SubtractCalculation, 10.0, 5.0, 5.0, 'subtraction'),
        (SubtractCalculation, -10.0, -5.0, -5.0, 'subtraction'),
        (MultiplyCalculation, 10.0, 5.0, 50.0, 'multiplication'),
        (MultiplyCalculation, -10.0, 5.0, -50.0, 'multiplication'),
        (DivideCalculation, 10.0, 5.0, 2.0, 'division'),
        (DivideCalculation, -10.0, -5.0, 2.0, 'division'),
        (DivideCalculation, 1e308, 1e-308, 1e616, 'division'),  # Edge case: very large / very small
    ]
)
@patch.object(Operation, 'addition')
@patch.object(Operation, 'subtraction')
@patch.object(Operation, 'multiplication')
@patch.object(Operation, 'division')
def test_calculation_execute_positive(
    mock_division, mock_multiplication, mock_subtraction, mock_addition,
    calc_class, a, b, expected, mock_method
):
    """
    Parameterized positive execution tests for all Calculation classes.
    Edge cases included: negative numbers, large/small numbers.
    """
    # Arrange: assign expected return value to the correct Operation method
    getattr(locals()[f'mock_{mock_method}'], 'return_value', None)
    if mock_method == 'addition':
        mock_addition.return_value = expected
    elif mock_method == 'subtraction':
        mock_subtraction.return_value = expected
    elif mock_method == 'multiplication':
        mock_multiplication.return_value = expected
    elif mock_method == 'division':
        mock_division.return_value = expected

    # Act
    calc = calc_class(a, b)
    result = calc.execute()

    # Assert
    assert result == expected
    if mock_method == 'addition':
        mock_addition.assert_called_once_with(a, b)
    elif mock_method == 'subtraction':
        mock_subtraction.assert_called_once_with(a, b)
    elif mock_method == 'multiplication':
        mock_multiplication.assert_called_once_with(a, b)
    elif mock_method == 'division':
        mock_division.assert_called_once_with(a, b)


# -----------------------------------------------------------------------------------
# Parameterized Negative Execution Tests (Exceptions)
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, a, b, mock_method, exception_msg",
    [
        (AddCalculation, 10.0, 5.0, 'addition', "Addition error"),
        (SubtractCalculation, 10.0, 5.0, 'subtraction', "Subtraction error"),
        (MultiplyCalculation, 10.0, 5.0, 'multiplication', "Multiplication error"),
        (DivideCalculation, 10.0, 5.0, 'division', "Division error"),
    ]
)
@patch.object(Operation, 'addition')
@patch.object(Operation, 'subtraction')
@patch.object(Operation, 'multiplication')
@patch.object(Operation, 'division')
def test_calculation_execute_exceptions(
    mock_division, mock_multiplication, mock_subtraction, mock_addition,
    calc_class, a, b, mock_method, exception_msg
):
    """
    Parameterized negative execution tests for all Calculation classes.
    Each Operation method is mocked to raise an exception.
    """
    # Arrange: set the correct Operation method to raise exception
    if mock_method == 'addition':
        mock_addition.side_effect = Exception(exception_msg)
    elif mock_method == 'subtraction':
        mock_subtraction.side_effect = Exception(exception_msg)
    elif mock_method == 'multiplication':
        mock_multiplication.side_effect = Exception(exception_msg)
    elif mock_method == 'division':
        mock_division.side_effect = Exception(exception_msg)

    # Act & Assert
    calc = calc_class(a, b)
    with pytest.raises(Exception) as exc_info:
        calc.execute()
    assert str(exc_info.value) == exception_msg


# -----------------------------------------------------------------------------------
# Parameterized Division by Zero Test
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, a, b",
    [
        (DivideCalculation, 10.0, 0.0),
        (DivideCalculation, -5.0, 0.0),
        (DivideCalculation, 0.0, 0.0)
    ]
)
def test_divide_by_zero(calc_class, a, b):
    """
    Parameterized test for DivideCalculation division by zero.
    Ensures ZeroDivisionError is raised with correct message.
    """
    calc = calc_class(a, b)
    with pytest.raises(ZeroDivisionError) as exc_info:
        calc.execute()
    assert str(exc_info.value) == "Cannot divide by zero."


# -----------------------------------------------------------------------------------
# Parameterized Factory Creation Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_type, expected_class",
    [
        ('add', AddCalculation),
        ('subtract', SubtractCalculation),
        ('multiply', MultiplyCalculation),
        ('divide', DivideCalculation)
    ]
)
def test_factory_creates_instances(calc_type, expected_class):
    """
    Parameterized tests to verify that CalculationFactory creates correct instances.
    """
    a, b = 10.0, 5.0
    calc = CalculationFactory.create_calculation(calc_type, a, b)
    assert isinstance(calc, expected_class)
    assert calc.a == a
    assert calc.b == b


@pytest.mark.parametrize(
    "unsupported_type",
    ['modulus', 'power', 'sqrt']
)
def test_factory_unsupported_type(unsupported_type):
    """
    Parameterized tests to verify that requesting unsupported calculation type raises ValueError.
    """
    a, b = 10.0, 5.0
    with pytest.raises(ValueError) as exc_info:
        CalculationFactory.create_calculation(unsupported_type, a, b)
    assert unsupported_type in str(exc_info.value)


# -----------------------------------------------------------------------------------
# Parameterized String Representation (__str__) Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, a, b, expected_str, mock_method, mock_value",
    [
        (AddCalculation, 10.0, 5.0, "AddCalculation: 10.0 Add 5.0 = 15.0", 'addition', 15.0),
        (SubtractCalculation, 10.0, 5.0, "SubtractCalculation: 10.0 Subtract 5.0 = 5.0", 'subtraction', 5.0),
        (MultiplyCalculation, 10.0, 5.0, "MultiplyCalculation: 10.0 Multiply 5.0 = 50.0", 'multiplication', 50.0),
        (DivideCalculation, 10.0, 5.0, "DivideCalculation: 10.0 Divide 5.0 = 2.0", 'division', 2.0)
    ]
)
@patch.object(Operation, 'addition', return_value=15.0)
@patch.object(Operation, 'subtraction', return_value=5.0)
@patch.object(Operation, 'multiplication', return_value=50.0)
@patch.object(Operation, 'division', return_value=2.0)
def test_calculation_str(
    mock_division, mock_multiplication, mock_subtraction, mock_addition,
    calc_class, a, b, expected_str, mock_method, mock_value
):
    """
    Parameterized __str__ tests for Calculation subclasses.
    Verifies string formatting for different operations.
    """
    calc = calc_class(a, b)
    calc_str = str(calc)
    assert calc_str == expected_str


# -----------------------------------------------------------------------------------
# Parameterized Repr Representation (__repr__) Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, a, b, expected_repr",
    [
        (AddCalculation, 10.0, 5.0, "AddCalculation(a=10.0, b=5.0)"),
        (SubtractCalculation, 10.0, 5.0, "SubtractCalculation(a=10.0, b=5.0)"),
        (MultiplyCalculation, 10.0, 5.0, "MultiplyCalculation(a=10.0, b=5.0)"),
        (DivideCalculation, 10.0, 5.0, "DivideCalculation(a=10.0, b=5.0)")
    ]
)
def test_calculation_repr(calc_class, a, b, expected_repr):
    """
    Parameterized __repr__ tests for Calculation subclasses.
    Verifies repr formatting for all operations.
    """
    calc = calc_class(a, b)
    assert repr(calc) == expected_repr


# -----------------------------------------------------------------------------------
# Parameterized Factory Duplicate Registration Test
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "existing_type",
    ['add', 'subtract', 'multiply', 'divide']
)
def test_factory_register_duplicate(existing_type):
    """
    Parameterized test to ensure duplicate calculation registration raises ValueError.
    """
    with pytest.raises(ValueError) as exc_info:
        @CalculationFactory.register_calculation(existing_type)
        class DummyCalculation(Calculation):
            def execute(self):
                return 0.0
    assert f"Calculation type '{existing_type}' is already registered." in str(exc_info.value)
