"""
PYTHON OBJECT-ORIENTED PROGRAMMING: FROM BASIC TO ADVANCED
==========================================================

This comprehensive guide covers Python's OOP features with examples, analogies, and detailed comments.
Each section builds upon the previous one, progressing from basic to advanced concepts.
"""

# ==========================================================
# SECTION 1: BASIC CLASS DEFINITION AND OBJECTS
# ==========================================================

"""
ANALOGY: Think of a class as a blueprint for a house. The blueprint defines what the house 
will have (attributes) and what can be done in it (methods). An object is an actual house 
built from that blueprint.
"""

class Dog:
    """
    A simple class representing a dog.
    
    This demonstrates the most basic class definition in Python.
    """
    # Class attribute - shared by all instances
    species = "Canis familiaris"
    # The __init__ method is a special method called when an object is created
    # It's similar to a constructor in other programming languages
    def __init__(self, name, age):
        """Initialize a new Dog object.
        
        Args:
            name (str): The dog's name
            age (int): The dog's age in years
        """
        # Instance attributes - unique to each instance
        self.name = name  # 'self' refers to the instance being created
        self.age = age
    # Instance method - defines behavior
    def bark(self):
        """The dog makes a sound."""
        return f"{self.name} says Woof!"
    # Another instance method
    def get_info(self):
        """Return a string with the dog's information."""
        return f"{self.name} is {self.age} years old."

# Creating objects (instances) of the Dog class
fido = Dog("Fido", 3)
bella = Dog("Bella", 5)

# Accessing attributes
print(fido.name)        # Output: Fido
print(bella.age)        # Output: 5
print(fido.species)     # Output: Canis familiaris

# Calling methods
print(fido.bark())      # Output: Fido says Woof!
print(bella.get_info()) # Output: Bella is 5 years old.


# ==========================================================
# SECTION 2: INHERITANCE
# ==========================================================

"""
ANALOGY: Inheritance is like genetic inheritance. A child inherits traits from their parents
but may also have unique characteristics. Similarly, a subclass inherits attributes and methods
from its parent class but can also have its own unique attributes and methods.
"""

class Pet:
    """A base class for all pets."""
    
    def __init__(self, name, age):
        """Initialize a Pet object.
        
        Args:
            name (str): The pet's name
            age (int): The pet's age in years
        """
        self.name = name
        self.age = age
    
    def speak(self):
        """The sound the pet makes (to be overridden by subclasses)."""
        return "Some generic pet sound"
    
    def __str__(self):
        """Return a string representation of the pet."""
        return f"{self.name}, age {self.age}"


class Cat(Pet):  # Cat inherits from Pet
    """A class representing a cat, inheriting from Pet."""
    
    species = "Felis catus"
    
    def __init__(self, name, age, color):
        """Initialize a Cat object.
        
        Args:
            name (str): The cat's name
            age (int): The cat's age in years
            color (str): The cat's fur color
        """
        # Call the parent class's __init__ method
        super().__init__(name, age)
        # Add attributes specific to Cat
        self.color = color
    
    def speak(self):
        """Override the speak method from the parent class."""
        return f"{self.name} says Meow!"
    
    def purr(self):
        """A method specific to cats."""
        return f"{self.name} purrs contentedly."


# Creating instances
whiskers = Cat("Whiskers", 4, "gray")

# Cat inherits from Pet
print(isinstance(whiskers, Cat))   # Output: True
print(isinstance(whiskers, Pet))   # Output: True

# Accessing inherited and specific attributes
print(whiskers.name)   # From Pet
print(whiskers.color)  # From Cat

# Calling inherited, overridden, and specific methods
print(whiskers)         # Calls __str__ from Pet, Output: Whiskers, age 4
print(whiskers.speak()) # Calls overridden speak method, Output: Whiskers says Meow!
print(whiskers.purr())  # Calls Cat-specific method, Output: Whiskers purrs contentedly.


# ==========================================================
# SECTION 3: ENCAPSULATION
# ==========================================================

"""
ANALOGY: Encapsulation is like a car's engine covered by a hood. Users don't need to know how
the engine works internally; they just use the steering wheel, pedals, etc. (the public interface).
Similarly, objects can hide their internal state and require other objects to interact with them
through their public methods.
"""

class BankAccount:
    """A class representing a bank account with private attributes."""
    
    def __init__(self, owner, initial_balance=0):
        """Initialize a BankAccount object.
        
        Args:
            owner (str): The account owner's name
            initial_balance (float, optional): The starting balance
        """
        self.owner = owner
        # Private attribute (by convention) - use double underscore prefix
        self.__balance = initial_balance
        # Protected attribute (by convention) - use single underscore prefix
        self._transaction_count = 0
    
    def deposit(self, amount):
        """Deposit money into the account.
        
        Args:
            amount (float): The amount to deposit
            
        Returns:
            float: The new balance
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.__balance += amount
        self._transaction_count += 1
        return self.__balance
    
    def withdraw(self, amount):
        """Withdraw money from the account.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            float: The new balance
            
        Raises:
            ValueError: If amount is negative or exceeds balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        
        self.__balance -= amount
        self._transaction_count += 1
        return self.__balance
    
    def get_balance(self):
        """Get the current balance.
        
        Returns:
            float: The current balance
        """
        return self.__balance
    
    def get_transaction_count(self):
        """Get the number of transactions.
        
        Returns:
            int: The number of transactions
        """
        return self._transaction_count


# Creating an account
account = BankAccount("John Doe", 1000)

# Using public methods to interact with the object
print(account.deposit(500))      # Output: 1500
print(account.withdraw(200))     # Output: 1300
print(account.get_balance())     # Output: 1300

# Trying to access private attribute directly would raise an AttributeError
# print(account.__balance)  # This would cause an AttributeError

# Name mangling - Python's way of implementing private attributes
# The attribute is accessible, but the name is changed
print(account._BankAccount__balance)  # Output: 1300 (not recommended in practice)

# Protected attributes are accessible but signal "don't touch directly"
print(account._transaction_count)     # Output: 2 (not recommended in practice)


# ==========================================================
# SECTION 4: POLYMORPHISM
# ==========================================================

"""
ANALOGY: Polymorphism is like a TV remote control. The same "power" button works on different
TV models and brands, but the actual implementation might be different for each. Similarly,
different classes can implement the same method name, and each will respond in its own way.
"""

class Animal:
    """Base class for all animals."""
    
    def __init__(self, name):
        """Initialize an Animal object.
        
        Args:
            name (str): The animal's name
        """
        self.name = name
    
    def speak(self):
        """The sound the animal makes (to be overridden by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def introduce(self):
        """The animal introduces itself."""
        return f"I am {self.name} and I {self.speak()}"


class Dog(Animal):
    """A class representing a dog."""
    
    def speak(self):
        """The sound a dog makes."""
        return "bark"


class Cat(Animal):
    """A class representing a cat."""
    
    def speak(self):
        """The sound a cat makes."""
        return "meow"


class Duck(Animal):
    """A class representing a duck."""
    
    def speak(self):
        """The sound a duck makes."""
        return "quack"


# Polymorphism in action
def animal_sound(animal):
    """Get the sound an animal makes.
    
    Args:
        animal (Animal): An animal object
        
    Returns:
        str: The sound the animal makes
    """
    return animal.speak()


# Creating different animal objects
fido = Dog("Fido")
whiskers = Cat("Whiskers")
donald = Duck("Donald")

# Same function works with different types of objects
print(animal_sound(fido))      # Output: bark
print(animal_sound(whiskers))  # Output: meow
print(animal_sound(donald))    # Output: quack

# The introduce method works with any Animal subclass
print(fido.introduce())       # Output: I am Fido and I bark
print(whiskers.introduce())   # Output: I am Whiskers and I meow
print(donald.introduce())     # Output: I am Donald and I quack


# ==========================================================
# SECTION 5: ABSTRACTION
# ==========================================================

"""
ANALOGY: Abstraction is like driving a car. You don't need to understand how the engine works
to drive it; you just need to know how to use the steering wheel, pedals, etc. Similarly,
abstract classes define a common interface without implementing all the details.
"""

from abc import ABC, abstractmethod

class Shape(ABC):
    """An abstract base class for geometric shapes.
    
    This class cannot be instantiated directly.
    """
    
    @abstractmethod
    def area(self):
        """Calculate the area of the shape.
        
        Returns:
            float: The area
        """
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate the perimeter of the shape.
        
        Returns:
            float: The perimeter
        """
        pass
    
    def describe(self):
        """Return a description of the shape.
        
        Returns:
            str: A description including area and perimeter
        """
        return f"This shape has an area of {self.area()} and a perimeter of {self.perimeter()}"


class Circle(Shape):
    """A class representing a circle."""
    
    def __init__(self, radius):
        """Initialize a Circle object.
        
        Args:
            radius (float): The circle's radius
        """
        self.radius = radius
    
    def area(self):
        """Calculate the area of the circle.
        
        Returns:
            float: The area
        """
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        """Calculate the perimeter (circumference) of the circle.
        
        Returns:
            float: The perimeter
        """
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    """A class representing a rectangle."""
    
    def __init__(self, width, height):
        """Initialize a Rectangle object.
        
        Args:
            width (float): The rectangle's width
            height (float): The rectangle's height
        """
        self.width = width
        self.height = height
    
    def area(self):
        """Calculate the area of the rectangle.
        
        Returns:
            float: The area
        """
        return self.width * self.height
    
    def perimeter(self):
        """Calculate the perimeter of the rectangle.
        
        Returns:
            float: The perimeter
        """
        return 2 * (self.width + self.height)


# Creating shape objects
circle = Circle(5)
rectangle = Rectangle(4, 6)

# Using the common interface
print(circle.area())        # Output: 78.53975
print(rectangle.area())     # Output: 24
print(circle.describe())    # Output: This shape has an area of 78.53975 and a perimeter of 31.4159
print(rectangle.describe()) # Output: This shape has an area of 24 and a perimeter of 20

# This would raise an error - can't instantiate abstract class
# shape = Shape()  # TypeError: Can't instantiate abstract class Shape with abstract methods area, perimeter


# ==========================================================
# SECTION 6: PROPERTIES AND DESCRIPTORS
# ==========================================================

"""
ANALOGY: Properties are like smart mailboxes that can perform checks when mail is deposited or 
retrieved. Similarly, properties let you add logic when attributes are accessed or modified.
"""

class Temperature:
    """A class representing a temperature with validation."""
    
    def __init__(self, celsius=0):
        """Initialize a Temperature object.
        
        Args:
            celsius (float, optional): The temperature in Celsius
        """
        # Use the setter to validate the initial value
        self.celsius = celsius
    
    @property
    def celsius(self):
        """Get the temperature in Celsius.
        
        This is a getter method that is called when the celsius attribute is accessed.
        
        Returns:
            float: The temperature in Celsius
        """
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Set the temperature in Celsius.
        
        This is a setter method that is called when the celsius attribute is assigned.
        
        Args:
            value (float): The temperature in Celsius
            
        Raises:
            ValueError: If the temperature is below absolute zero
        """
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Get the temperature in Fahrenheit.
        
        Returns:
            float: The temperature in Fahrenheit
        """
        return self.celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set the temperature in Fahrenheit.
        
        Args:
            value (float): The temperature in Fahrenheit
        """
        self.celsius = (value - 32) * 5/9


# Using properties
temp = Temperature(25)

# Accessing properties
print(temp.celsius)     # Output: 25
print(temp.fahrenheit)  # Output: 77.0

# Setting properties
temp.celsius = 30
print(temp.fahrenheit)  # Output: 86.0

temp.fahrenheit = 68
print(temp.celsius)     # Output: 20.0

# Validation
try:
    temp.celsius = -300  # This will raise a ValueError
except ValueError as e:
    print(f"Error: {e}")  # Output: Error: Temperature cannot be below absolute zero


# ==========================================================
# SECTION 7: CLASS AND STATIC METHODS
# ==========================================================

"""
ANALOGY: Class methods are like staff meetings that involve all employees but not the office 
building itself. Static methods are like using a company's conference room for a community 
meeting - they're associated with the company but don't involve the company or its employees.
"""

class MathOperations:
    """A class demonstrating class and static methods."""
    
    # Class variable
    pi = 3.14159
    
    def __init__(self, value):
        """Initialize the object with a value.
        
        Args:
            value (float): The value to store
        """
        self.value = value
    
    # Instance method - needs an instance (self)
    def add(self, x):
        """Add a number to the instance value.
        
        Args:
            x (float): The number to add
            
        Returns:
            float: The result
        """
        return self.value + x
    
    # Class method - needs the class (cls)
    @classmethod
    def circle_area(cls, radius):
        """Calculate the area of a circle.
        
        This method doesn't need an instance but uses the class variable pi.
        
        Args:
            radius (float): The radius of the circle
            
        Returns:
            float: The area of the circle
        """
        return cls.pi * radius ** 2
    
    # Another class method - can create instances
    @classmethod
    def create_zero(cls):
        """Create a new instance with a value of zero.
        
        Returns:
            MathOperations: A new instance
        """
        return cls(0)
    
    # Static method - doesn't need the class or an instance
    @staticmethod
    def is_positive(x):
        """Check if a number is positive.
        
        Args:
            x (float): The number to check
            
        Returns:
            bool: True if the number is positive, False otherwise
        """
        return x > 0


# Using instance methods
math_ops = MathOperations(10)
print(math_ops.add(5))  # Output: 15

# Using class methods
print(MathOperations.circle_area(5))  # Output: 78.53975

# Using class method to create an instance
zero_ops = MathOperations.create_zero()
print(zero_ops.value)  # Output: 0

# Using static methods
print(MathOperations.is_positive(10))  # Output: True
print(MathOperations.is_positive(-5))  # Output: False


# ==========================================================
# SECTION 8: MAGIC METHODS (DUNDER METHODS)
# ==========================================================

"""
ANALOGY: Magic methods are like the hidden controls of a game controller. When you press a button, 
specific actions happen behind the scenes. Similarly, magic methods are automatically called
in response to certain operations on objects.
"""

class Vector:
    """A 2D vector class with operator overloading."""
    
    def __init__(self, x, y):
        """Initialize a Vector object.
        
        Args:
            x (float): The x-coordinate
            y (float): The y-coordinate
        """
        self.x = x
        self.y = y
    
    # String representation
    def __str__(self):
        """Return a string representation of the vector.
        
        This is called by the str() function and when printing the object.
        
        Returns:
            str: A string representing the vector
        """
        return f"Vector({self.x}, {self.y})"
    
    # Formal representation
    def __repr__(self):
        """Return a formal string representation of the vector.
        
        This is called by the repr() function and in the REPL.
        
        Returns:
            str: A string that could be used to recreate the object
        """
        return f"Vector({self.x}, {self.y})"
    
    # Addition: v1 + v2
    def __add__(self, other):
        """Add two vectors.
        
        Args:
            other (Vector): The vector to add
            
        Returns:
            Vector: The sum of the vectors
        """
        return Vector(self.x + other.x, self.y + other.y)
    
    # Subtraction: v1 - v2
    def __sub__(self, other):
        """Subtract one vector from another.
        
        Args:
            other (Vector): The vector to subtract
            
        Returns:
            Vector: The difference of the vectors
        """
        return Vector(self.x - other.x, self.y - other.y)
    
    # Multiplication by scalar: v * scalar
    def __mul__(self, scalar):
        """Multiply the vector by a scalar.
        
        Args:
            scalar (float): The scalar to multiply by
            
        Returns:
            Vector: The scaled vector
        """
        return Vector(self.x * scalar, self.y * scalar)
    
    # Equality: v1 == v2
    def __eq__(self, other):
        """Check if two vectors are equal.
        
        Args:
            other (Vector): The vector to compare with
            
        Returns:
            bool: True if the vectors are equal, False otherwise
        """
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y
    
    # Length of vector: len(v)
    def __len__(self):
        """Return the length of the vector.
        
        Returns:
            int: The Euclidean length, truncated to an integer
        """
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
    
    # Make the object callable: v()
    def __call__(self, factor=1):
        """Scale the vector when the object is called.
        
        Args:
            factor (float, optional): The scaling factor
            
        Returns:
            Vector: The scaled vector
        """
        return Vector(self.x * factor, self.y * factor)


# Creating vectors
v1 = Vector(3, 4)
v2 = Vector(5, 6)

# String representation
print(v1)           # Output: Vector(3, 4) (calls __str__)
print(repr(v2))     # Output: Vector(5, 6) (calls __repr__)

# Operator overloading
v3 = v1 + v2
print(v3)           # Output: Vector(8, 10) (calls __add__, then __str__)

v4 = v2 - v1
print(v4)           # Output: Vector(2, 2) (calls __sub__, then __str__)

v5 = v1 * 2
print(v5)           # Output: Vector(6, 8) (calls __mul__, then __str__)

# Equality
print(v1 == Vector(3, 4))  # Output: True (calls __eq__)
print(v1 == v2)            # Output: False (calls __eq__)

# Length
print(len(v1))      # Output: 5 (calls __len__)

# Callable objects
v6 = v1(3)
print(v6)           # Output: Vector(9, 12) (calls __call__, then __str__)


# ==========================================================
# SECTION 9: METACLASSES
# ==========================================================

"""
ANALOGY: If classes are blueprints for objects, metaclasses are blueprints for classes. It's like
a factory that produces factories - the metaclass is a factory for creating class objects, which
in turn create instance objects.
"""

# Define a metaclass
class SingletonMeta(type):
    """A metaclass that ensures only one instance of a class exists."""
    
    # Dictionary to store singleton instances
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """Create a new instance or return the existing one.
        
        This method is called when the class is instantiated.
        
        Returns:
            object: The singleton instance
        """
        if cls not in cls._instances:
            # Create a new instance
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Use the metaclass
class Database(metaclass=SingletonMeta):
    """A database class with only one instance (singleton).
    
    The metaclass ensures that only one instance is created.
    """
    
    def __init__(self, host="localhost"):
        """Initialize the database connection.
        
        Args:
            host (str, optional): The database host
        """
        self.host = host
        print(f"Connecting to database on {self.host}...")
    
    def query(self, sql):
        """Execute a SQL query.
        
        Args:
            sql (str): The SQL query
            
        Returns:
            str: A message indicating the query was executed
        """
        return f"Executing '{sql}' on {self.host}"


# Using the singleton class
db1 = Database()  # Output: Connecting to database on localhost...
db2 = Database("example.com")  # No output - the second instantiation is ignored

# Both variables refer to the same object
print(db1 is db2)  # Output: True
print(db1.host)    # Output: localhost
print(db2.host)    # Output: localhost


# Another example of a metaclass
class LoggingMeta(type):
    """A metaclass that adds logging to class methods."""
    
    def __new__(mcs, name, bases, attributes):
        """Create a new class with logging added to methods.
        
        Args:
            mcs: The metaclass
            name: The name of the class being created
            bases: The base classes of the class being created
            attributes: The attributes of the class being created
            
        Returns:
            type: The new class
        """
        # Add logging to each method
        for attr_name, attr_value in attributes.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                attributes[attr_name] = LoggingMeta.add_logging(attr_value, name)
        
        # Create the class
        return super().__new__(mcs, name, bases, attributes)
    
    @staticmethod
    def add_logging(method, class_name):
        """Add logging to a method.
        
        Args:
            method: The method to add logging to
            class_name: The name of the class the method belongs to
            
        Returns:
            function: The method with logging added
        """
        def wrapper(*args, **kwargs):
            print(f"Calling {method.__name__} on {class_name}")
            result = method(*args, **kwargs)
            print(f"{method.__name__} returned {result}")
            return result
        return wrapper


# Use the LoggingMeta metaclass
class Math(metaclass=LoggingMeta):
    """A class with methods that log their calls."""
    
    def add(self, x, y):
        """Add two numbers.
        
        Args:
            x (float): The first number
            y (float): The second number
            
        Returns:
            float: The sum
        """
        return x + y
    
    def multiply(self, x, y):
        """Multiply two numbers.
        
        Args:
            x (float): The first number
            y (float): The second number
            
        Returns:
            float: The product
        """
        return x * y


# Using the class with logging
math = Math()
result = math.add(2, 3)
# Output:
# Calling add on Math
# add returned 5

result = math.multiply(4, 5)
# Output:
# Calling multiply on Math
# multiply returned 20


# ==========================================================
# SECTION 10: ADVANCED DESIGN PATTERNS
# ==========================================================

"""
ANALOGY: Design patterns are like recipes in cooking. They're standard solutions to common 
problems that have been refined over time. Just as a chef doesn't have to reinvent a soufflé 
recipe, a programmer doesn't have to reinvent a solution to a common design problem.
"""

# Singleton Pattern (alternative implementation)
class Singleton:
    """A class implementing the Singleton pattern using a class variable."""
    
    # Class variable to store the instance
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Create a new instance if one doesn't exist.
        
        Returns:
            Singleton: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, value=None):
        """Initialize the singleton instance.
        
        Args:
            value: A value to store
        """
        # Only initialize once
        if not hasattr(self, "initialized"):
            self.value = value
            self.initialized = True


# Factory Pattern
class AnimalFactory:
    """A factory class for creating animals."""
    
    @staticmethod
    def create_animal(animal_type, *args, **kwargs):
        """Create an animal of the specified type.
        
        Args:
            animal_type (str): The type of animal to create
            *args: Positional arguments to pass to the constructor
            **kwargs: Keyword arguments to pass to the constructor
            
        Returns:
            Animal: An animal object
            
        Raises:
            ValueError: If the animal type is not supported
        """
        if animal_type == "dog":
            return Dog(*args, **kwargs)
        elif animal_type == "cat":
            return Cat(*args, **kwargs)
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")


# Observer Pattern
class Subject:
    """A subject that observers can subscribe to."""
    
    def __init__(self):
        """Initialize the subject with an empty list of observers."""
        self._observers = []
    
    def attach(self, observer):
        """Attach an observer to the subject.
        
        Args:
            observer: The observer to attach
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Detach an observer from the subject.
        
        Args:
            observer: The observer to detach
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, *args, **kwargs):
        """Notify all observers.
        
        Args:
            *args: Positional arguments to pass to observers
            **kwargs: Keyword arguments to pass to observers
        """
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


class Observer:
    """An observer that can subscribe to a subject."""
    
    def update(self, subject, *args, **kwargs):
        """Update the observer.
        
        Args:
            subject: The subject that notified the observer
            *args: Positional arguments from the subject
            **kwargs: Keyword arguments from the subject
        """
        pass


class StockMarket(Subject):
    """A stock market that observers can subscribe to."""
    
    def __init__(self):
        """Initialize the stock market with a price."""
        super().__init__()
        self._price = 0
    
    @property
    def price(self):
        """Get the current stock price.
        
        Returns:
            float: The current price
        """
        return self._price
    
    @price.setter
    def price(self, value):
        """Set the stock price and notify observers.
        
        Args:
            value (float): The new price
        """
        self._price = value
        self.notify(value)


class Investor(Observer):
    """An investor that observes a stock market."""
    
    def __init__(self, name):
        """Initialize the investor with a name.
        
        Args:
            name (str): The investor's name
        """
        self.name = name
    
    def update(self, subject, *args, **kwargs):
        """Update the investor.
        
        Args:
            subject (StockMarket): The stock market that notified the investor
            *args: The new price
        """
        price = args[0]
        print(f"{self.name} noticed that the stock price changed to {price}")

