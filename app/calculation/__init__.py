# calculator_calculations.py

# -----------------------------------------------------------------------------------
# Import Statements
# -----------------------------------------------------------------------------------

# Import ABC (Abstract Base Class) and abstractmethod from Python's abc module.
# Abstract Base Classes (ABCs) allow us to define a contract for our subclasses, specifying 
# methods that they must implement. This helps in establishing a standard interface for 
# similar objects without enforcing specific details on how they should work.
from abc import ABC, abstractmethod

# Import the Operation class from the app.operation module. 
# The Operation class is where our basic mathematical functions (e.g., addition, subtraction) are defined.
# Rather than implementing arithmetic logic within each calculation class, we encapsulate it in a 
# separate class to promote modularity. This makes it easier to modify or extend these functions independently.
from app.operation import Operation

# -----------------------------------------------------------------------------------
# Abstract Base Class: Calculation
# -----------------------------------------------------------------------------------
class Calculation(ABC):
    """
    The Calculation class is an Abstract Base Class (ABC) that defines a blueprint 
    for all mathematical calculations in the calculator program. This class establishes 
    a consistent interface that all calculation types (such as addition, subtraction, etc.) 
    must follow. 
    
    """

    def __init__(self, a: float, b: float) -> None:
        """
        Initializes a Calculation instance with two operands (numbers involved in the calculation).
        
        **Parameters:**
        - `a (float)`: The first operand.
        - `b (float)`: The second operand.
        """
        self.a: float = a  # Stores the first operand as a floating-point number.
        self.b: float = b  # Stores the second operand as a floating-point number.

    @abstractmethod
    def execute(self) -> float:
        """
        Abstract method to perform the calculation. Subclasses will provide specific 
        implementations of this method, defining the arithmetic for each operation.

        **Returns:**
        - `float`: The result of the calculation.
        """
        pass  # The actual implementation will be provided by the subclass. # pragma: no cover

    def __str__(self) -> str:
        """
        Provides a user-friendly string representation of the Calculation instance, 
        showing the operation name, operands, and result. This enhances **Readability** 
        and **Debugging** by giving a clear output for each calculation.

        **Returns:**
        - `str`: A string describing the calculation and its result.
        """
        result = self.execute()  # Run the calculation to get the result.
        operation_name = self.__class__.__name__.replace('Calculation', '')  # Derive operation name.
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"

    def __repr__(self) -> str:
        """
        Provides a technical, unambiguous representation of the Calculation instance 
        showing the class name and operand values. This is useful for debugging 
        since it gives a clear and consistent format for all Calculation objects.

        **Returns:**
        - `str`: A string containing the class name and operands.
        """
        return f"{self.__class__.__name__}(a={self.a}, b={self.b})"

# -----------------------------------------------------------------------------------
# Factory Class: CalculationFactory
# -----------------------------------------------------------------------------------
class CalculationFactory:
    """
    The CalculationFactory is a **Factory Class** responsible for creating instances 
    of Calculation subclasses. This design pattern allows us to encapsulate the 
    logic of object creation and make it flexible.

    """

    # _calculations is a dictionary that holds a mapping of calculation types 
    # (like "add" or "subtract") to their respective classes.
    _calculations = {}

    @classmethod
    def register_calculation(cls, calculation_type: str):
        """
        This method is a decorator used to register a specific Calculation subclass 
        under a unique calculation type. Registering classes with string identifiers 
        like "add" or "multiply" enables easy access to different operations 
        dynamically at runtime.

        **Parameters:**
        - `calculation_type (str)`: A short identifier for the type of calculation 
          (e.g., 'add' for addition).
        
        """
        def decorator(subclass):
            # Convert calculation_type to lowercase to ensure consistency.
            calculation_type_lower = calculation_type.lower()
            # Check if the calculation type has already been registered to avoid duplication.
            if calculation_type_lower in cls._calculations:
                raise ValueError(f"Calculation type '{calculation_type}' is already registered.")
            # Register the subclass in the _calculations dictionary.
            cls._calculations[calculation_type_lower] = subclass
            return subclass  # Return the subclass for chaining or additional use.
        return decorator  # Return the decorator function.

    @classmethod
    def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
        """
        Factory method that creates instances of Calculation subclasses based on 
        a specified calculation type.

        **Parameters:**
        - `calculation_type (str)`: The type of calculation ('add', 'subtract', 'multiply', 'divide').
        - `a (float)`: The first operand.
        - `b (float)`: The second operand.
        
        **Returns:**
        - `Calculation`: An instance of the appropriate Calculation subclass.

        """
        calculation_type_lower = calculation_type.lower()
        calculation_class = cls._calculations.get(calculation_type_lower)
        # If the type is unsupported, raise an error with the available types.
        if not calculation_class:
            available_types = ', '.join(cls._calculations.keys())
            raise ValueError(f"Unsupported calculation type: '{calculation_type}'. Available types: {available_types}")
        # Create and return an instance of the requested calculation class with the provided operands.
        return calculation_class(a, b)

# -----------------------------------------------------------------------------------
# Concrete Calculation Classes
# -----------------------------------------------------------------------------------

# Each of these classes defines a specific calculation type (addition, subtraction, 
# multiplication, or division). These classes inherit from Calculation, implementing 
# the `execute` method to perform the specific arithmetic operation. 

@CalculationFactory.register_calculation('add')
class AddCalculation(Calculation):
    """
    AddCalculation represents an addition operation between two numbers.
    
    """

    def execute(self) -> float:
        # Calls the addition method from the Operation module to perform the addition.
        return Operation.addition(self.a, self.b)


@CalculationFactory.register_calculation('subtract')
class SubtractCalculation(Calculation):
    """
    SubtractCalculation represents a subtraction operation between two numbers.
    
    **Implementation Note**: This class specifically handles subtraction, keeping 
    the implementation separate from other operations.
    """

    def execute(self) -> float:
        # Calls the subtraction method from the Operation module to perform the subtraction.
        return Operation.subtraction(self.a, self.b)


@CalculationFactory.register_calculation('multiply')
class MultiplyCalculation(Calculation):
    """
    MultiplyCalculation represents a multiplication operation.
    
    By encapsulating the multiplication logic here, we achieve a clear separation of 
    concerns, making it easy to adjust the multiplication logic without affecting other calculations.
    """

    def execute(self) -> float:
        # Calls the multiplication method from the Operation module to perform the multiplication.
        return Operation.multiplication(self.a, self.b)


@CalculationFactory.register_calculation('divide')
class DivideCalculation(Calculation):
    """
    DivideCalculation represents a division operation.
    
    **Special Case - Division by Zero**: Division requires extra error handling to 
    prevent dividing by zero, which would cause an error in the program. This class 
    checks if the second operand is zero before performing the operation.
    """

    def execute(self) -> float:
        # Before performing division, check if `b` is zero to avoid ZeroDivisionError.
        if self.b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        # Calls the division method from the Operation module to perform the division.
        return Operation.division(self.a, self.b)

@CalculationFactory.register_calculation('power')
class PowerCalculation(Calculation):
    """
    PowerCalculation represents an exponentiation operation.

    By encapsulating the exponentiation logic here, we achieve a clear separation of
    concerns, making it easy to adjust the exponentiation logic without affecting other calculations.
    """
    def execute(self) -> float:
        # Calls the power method from the Operation module to perform the exponentiation .
        return Operation.power(self.a, self.b) # pragma: no cover