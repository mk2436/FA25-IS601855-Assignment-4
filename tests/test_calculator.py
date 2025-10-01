"""
Fully parameterized unit tests for the 'app/calculator.py' module using pytest.

Covers:
- display_help
- display_history
- Calculator REPL commands
- Arithmetic operations
- Division by zero
- Invalid input
- Unsupported operations
- Exceptional cases: KeyboardInterrupt, EOFError, unexpected exceptions

All tests follow the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from io import StringIO
from app.calculator import display_help, display_history, calculator

# -----------------------------------------------------------------------------------
# display_help Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "function, expected_snippets",
    [
        (
            display_help,
            ["Calculator REPL Help", "Usage:", "Special Commands:", "Examples:"]
        ),
    ],
)
def test_display_help_parametrized(function, expected_snippets, capsys):
    """
    Parameterized test for display_help function.
    Verifies that key sections of the help message are printed.
    """
    # Act
    function()
    captured = capsys.readouterr()

    # Assert
    for snippet in expected_snippets:
        assert snippet in captured.out

# -----------------------------------------------------------------------------------
# display_history Tests
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "history, expected_output",
    [
        ([], "No calculations performed yet."),  # Empty history
        (
            [
                "AddCalculation: 10.0 Add 5.0 = 15.0",
                "SubtractCalculation: 20.0 Subtract 3.0 = 17.0",
            ],
            "Calculation History:\n"
            "1. AddCalculation: 10.0 Add 5.0 = 15.0\n"
            "2. SubtractCalculation: 20.0 Subtract 3.0 = 17.0",
        ),
    ],
)
def test_display_history_parametrized(history, expected_output, capsys):
    """
    Parameterized test for display_history function.
    Handles empty and non-empty history lists.
    """
    # Act
    display_history(history)
    captured = capsys.readouterr()

    # Assert
    assert captured.out.strip() == expected_output.strip()

# -----------------------------------------------------------------------------------
# Calculator REPL Tests (commands, arithmetic, invalid input)
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "user_inputs, expected_outputs",
    [
        # Exit command
        ("exit\n", ["Exiting calculator. Goodbye!"]),

        # Help command
        ("help\nexit\n", ["Calculator REPL Help", "Exiting calculator. Goodbye!"]),

        # Invalid input format
        ("invalid input\nadd 5\nsubtract\nexit\n",
         ["Invalid input. Please follow the format: <operation> <num1> <num2>",
          "Type 'help' for more information."]),

        # Arithmetic operations
        ("add 10 5\nexit\n", ["Result: AddCalculation: 10.0 Add 5.0 = 15.0"]),
        ("subtract 20 5\nexit\n", ["Result: SubtractCalculation: 20.0 Subtract 5.0 = 15.0"]),
        ("multiply 7 8\nexit\n", ["Result: MultiplyCalculation: 7.0 Multiply 8.0 = 56.0"]),
        ("divide 20 4\nexit\n", ["Result: DivideCalculation: 20.0 Divide 4.0 = 5.0"]),

        # Division by zero
        ("divide 10 0\nexit\n", ["Cannot divide by zero."]),

        # History
        ("add 10 5\nsubtract 20 3\nhistory\nexit\n",
         ["Result: AddCalculation: 10.0 Add 5.0 = 15.0",
          "Result: SubtractCalculation: 20.0 Subtract 3.0 = 17.0",
          "Calculation History:"]),

        # Invalid numbers
        ("add ten five\nexit\n", [
            "Invalid input. Please follow the format: <operation> <num1> <num2>",
            "Type 'help' for more information."
        ]),

        # Unsupported operation
        ("modulus 2 3\nexit\n", [
            "Unsupported calculation type: 'modulus'.",
            "Type 'help' to see the list of supported operations."
        ]),
    ],
)
def test_calculator_repl_parametrized(monkeypatch, capsys, user_inputs, expected_outputs):
    """
    Fully parameterized test for calculator REPL.
    Covers: exit, help, history, arithmetic operations, invalid input, division by zero, unsupported operations.
    """
    # Arrange
    monkeypatch.setattr('sys.stdin', StringIO(user_inputs))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    for expected in expected_outputs:
        assert expected in captured.out

# -----------------------------------------------------------------------------------
# Exceptional Cases (KeyboardInterrupt and EOFError)
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "exception, expected_message",
    [
        (KeyboardInterrupt, "\nKeyboard interrupt detected. Exiting calculator. Goodbye!"),
        (EOFError, "\nEOF detected. Exiting calculator. Goodbye!"),
    ],
)
def test_calculator_exceptions_parametrized(monkeypatch, capsys, exception, expected_message):
    """
    Parameterized test for KeyboardInterrupt and EOFError in calculator REPL.
    Ensures graceful exit with correct message.
    """
    # Arrange
    def mock_input(prompt):
        raise exception()
    monkeypatch.setattr('builtins.input', mock_input)

    # Act
    with pytest.raises(SystemExit) as exc_info:
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert expected_message in captured.out
    assert exc_info.value.code == 0

# -----------------------------------------------------------------------------------
# Unexpected Exception Handling
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "exception_message",
    [
        ("Mock exception during execution",)
    ],
)
def test_calculator_unexpected_exception_parametrized(monkeypatch, capsys, exception_message):
    """
    Parameterized test for unexpected exceptions during calculation execution.
    """
    # Arrange
    class MockCalculation:
        def execute(self):
            raise Exception(exception_message[0])
        def __str__(self):
            return "MockCalculation"

    def mock_create_calculation(operation, a, b):
        return MockCalculation()

    monkeypatch.setattr('app.calculation.CalculationFactory.create_calculation', mock_create_calculation)
    user_input = 'add 10 5\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert f"An error occurred during calculation: {exception_message[0]}" in captured.out
    assert "Please try again." in captured.out



# -----------------------------------------------------------------------------------
# REPL Command Edge Cases
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "user_inputs, expected_outputs",
    [
        # Exit command
        ("exit\n", ["Exiting calculator. Goodbye!"]),

        # Repeated exit command
        ("exit\nexit\n", ["Exiting calculator. Goodbye!"]),

        # Help command
        ("help\nexit\n", ["Calculator REPL Help", "Exiting calculator. Goodbye!"]),

        # History with empty list
        ("history\nexit\n", ["No calculations performed yet.", "Exiting calculator. Goodbye!"]),
    ],
)
def test_repl_commands(monkeypatch, capsys, user_inputs, expected_outputs):
    """
    Parameterized tests for REPL commands.
    Verifies correct behavior for exit, help, and history commands.
    """
    # Arrange
    monkeypatch.setattr('sys.stdin', StringIO(user_inputs))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    for expected in expected_outputs:
        assert expected in captured.out

# -----------------------------------------------------------------------------------
# Malformed or Unsupported Input
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "user_inputs, expected_outputs",
    [
        # Missing operands
        ("add 5\nexit\n", [
            "Invalid input. Please follow the format: <operation> <num1> <num2>",
            "Type 'help' for more information."
        ]),
        ("subtract\nexit\n", [
            "Invalid input. Please follow the format: <operation> <num1> <num2>",
            "Type 'help' for more information."
        ]),

        # Extra operands
        ("add 1 2 3\nexit\n", [
            "Invalid input. Please follow the format: <operation> <num1> <num2>",
            "Type 'help' for more information."
        ]),

        # Unsupported operations
        ("modulus 10 3\nexit\n", [
            "Unsupported calculation type: 'modulus'.",
            "Type 'help' to see the list of supported operations."
        ]),
        ("foobar 1 2\nexit\n", [
            "Unsupported calculation type: 'foobar'.",
            "Type 'help' to see the list of supported operations."
        ]),
    ],
)
def test_repl_malformed_or_unsupported(monkeypatch, capsys, user_inputs, expected_outputs):
    """
    Parameterized tests for malformed input or unsupported operations.
    Ensures the REPL prints correct error messages and exits gracefully.
    """
    # Arrange
    monkeypatch.setattr('sys.stdin', StringIO(user_inputs))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    for expected in expected_outputs:
        assert expected in captured.out



# -----------------------------------------------------------------------------------
# Invalid Numeric Input
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "user_inputs, expected_outputs",
    [
        ("add ten five\nexit\n", [
            "Invalid input. Please follow the format: <operation> <num1> <num2>",
            "Type 'help' for more information."
        ]),
        ("multiply 2 two\nexit\n", [
            "Invalid input. Please follow the format: <operation> <num1> <num2>",
            "Type 'help' for more information."
        ]),
    ],
)
def test_repl_invalid_numeric(monkeypatch, capsys, user_inputs, expected_outputs):
    """
    Parameterized tests for invalid numeric input.
    Verifies that REPL handles non-numeric values correctly.
    """
    # Arrange
    monkeypatch.setattr('sys.stdin', StringIO(user_inputs))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    for expected in expected_outputs:
        assert expected in captured.out
