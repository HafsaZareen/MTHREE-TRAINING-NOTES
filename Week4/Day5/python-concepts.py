import random
import time
import functools
import itertools
import collections
import json
import re
import os
import sys
import threading
import concurrent.futures
import contextlib
from typing import List, Dict, Tuple, Set, Optional, Union, Callable, Generator, Any


class PythonConceptsShowcase:
    """
    A comprehensive class demonstrating various Python concepts beyond basic syntax.
    """
    
    def __init__(self, name: str = "Python Explorer"):
        """Initialize with various data types for demonstrations"""
        self.name = name
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.student_grades = {'Alice': 92, 'Bob': 85, 'Charlie': 78, 'David': 95, 'Eve': 88}
        self.data_tuple = (10, 20, 30, 40, 50)
        self.unique_items = {1, 3, 5, 7, 9}
        self._private_var = "I'm private"
        
    def run_all_demos(self) -> None:
        """Run all demonstration methods in sequence"""
        print(f"\n{'='*50}\nWelcome to the {self.name}!\n{'='*50}")
        
        demos = [
            self.demo_list_comprehensions,
            self.demo_dictionary_comprehensions,
            self.demo_generators,
            self.demo_iterators,
            self.demo_lambda_functions,
            self.demo_decorators,
            self.demo_higher_order_functions,
            self.demo_closures,
            self.demo_error_handling,
            self.demo_context_managers,
            self.demo_unpacking,
            self.demo_functional_tools,
            self.demo_advanced_functions,
            self.demo_regular_expressions,
            self.demo_collections_module,
            self.demo_threading,
            self.demo_type_hints,
        ]
        
        for i, demo in enumerate(demos, 1):
            print(f"\n{'-'*50}\nDemo {i}: {demo.__name__.replace('demo_', '').replace('_', ' ').title()}\n{'-'*50}")
            demo()
            time.sleep(0.5)  # Brief pause between demos
            
        print(f"\n{'='*50}\nAll demonstrations completed!\n{'='*50}")

    # List and Dictionary Comprehensions
    def demo_list_comprehensions(self) -> None:
        """Demonstrate list comprehensions"""
        # Basic list comprehension
        squares = [x**2 for x in self.numbers]
        print(f"Squares of numbers: {squares}")
        
        # List comprehension with condition
        even_squares = [x**2 for x in self.numbers if x % 2 == 0]
        print(f"Squares of even numbers: {even_squares}")
        
        # Nested list comprehension
        flattened = [item for sublist in self.nested_list for item in sublist]
        print(f"Flattened nested list: {flattened}")
        
        # List comprehension with conditional expression
        parity = ["even" if x % 2 == 0 else "odd" for x in self.numbers]
        print(f"Parity of numbers: {parity}")

    def demo_dictionary_comprehensions(self) -> None:
        """Demonstrate dictionary comprehensions"""
        # Basic dictionary comprehension
        squared_dict = {x: x**2 for x in self.numbers}
        print(f"Number to square mapping: {squared_dict}")
        
        # Dictionary comprehension with condition
        passing_students = {name: grade for name, grade in self.student_grades.items() if grade >= 85}
        print(f"Passing students: {passing_students}")
        
        # Swapping keys and values
        swapped = {grade: name for name, grade in self.student_grades.items()}
        print(f"Grades to names: {swapped}")
        
        # Creating a dictionary from lists
        letters = ['a', 'b', 'c', 'd']
        indices = {letter: index for index, letter in enumerate(letters)}
        print(f"Letter indices: {indices}")

    # Generators and Iterators
    def demo_generators(self) -> None:
        """Demonstrate generators and yield statements"""
        def fibonacci(n):
            """Generator for Fibonacci sequence"""
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b
        
        print(f"First 10 Fibonacci numbers: {list(fibonacci(10))}")
        
        # Generator expression
        gen_expr = (x**3 for x in self.numbers)
        print(f"First 3 cubes (generator): {next(gen_expr)}, {next(gen_expr)}, {next(gen_expr)}")
        
        # Generator with multiple yields
        def number_and_square(numbers):
            for n in numbers:
                yield n
                yield n**2
        
        print("Numbers and their squares interleaved:")
        for item in number_and_square([1, 2, 3]):
            print(item, end=" ")
        print()

    def demo_iterators(self) -> None:
        """Demonstrate custom iterators"""
        # Custom iterator class
        class CountDown:
            def __init__(self, start):
                self.count = start
                
            def __iter__(self):
                return self
                
            def __next__(self):
                if self.count <= 0:
                    raise StopIteration
                self.count -= 1
                return self.count + 1
        
        print("Custom iterator countdown from 5:")
        for i in CountDown(5):
            print(i, end=" ")
        print()
        
        # Using built-in iterators
        print("Using itertools.cycle for repeating pattern:")
        cycle = itertools.cycle([1, 2, 3])
        for _ in range(7):
            print(next(cycle), end=" ")
        print()

    # Lambda Functions and Functional Programming
    def demo_lambda_functions(self) -> None:
        """Demonstrate lambda functions"""
        # Basic lambda
        double = lambda x: x * 2
        print(f"Double of 5: {double(5)}")
        
        # Lambda with multiple arguments
        point_distance = lambda x1, y1, x2, y2: ((x2-x1)**2 + (y2-y1)**2)**0.5
        print(f"Distance between points (0,0) and (3,4): {point_distance(0, 0, 3, 4)}")
        
        # Lambda with conditional expression
        grade_status = lambda grade: "Pass" if grade >= 70 else "Fail"
        print(f"Status for grade 65: {grade_status(65)}")
        print(f"Status for grade 85: {grade_status(85)}")
        
        # Using lambda with map and filter
        numbers = [1, 2, 3, 4, 5]
        squared = list(map(lambda x: x**2, numbers))
        evens = list(filter(lambda x: x % 2 == 0, numbers))
        print(f"Squared using map: {squared}")
        print(f"Evens using filter: {evens}")

    # Decorators and Higher-Order Functions
    def demo_decorators(self) -> None:
        """Demonstrate decorators"""
        # Simple decorator to measure execution time
        def timer_decorator(func):
            @functools.wraps(func)  # Preserves function metadata
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds to run")
                return result
            return wrapper
        
        # Apply decorator to a test function
        @timer_decorator
        def slow_function(delay):
            time.sleep(delay)
            return "Function completed"
        
        print(slow_function(0.5))
        
        # Decorator with arguments
        def repeat(n):
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    results = []
                    for _ in range(n):
                        results.append(func(*args, **kwargs))
                    return results
                return wrapper
            return decorator
        
        @repeat(3)
        def say_hello(name):
            return f"Hello, {name}!"
        
        print(say_hello("Python"))

    def demo_higher_order_functions(self) -> None:
        """Demonstrate higher-order functions"""
        # Function that returns a function
        def get_multiplier(factor):
            def multiply(x):
                return x * factor
            return multiply
        
        double = get_multiplier(2)
        triple = get_multiplier(3)
        
        print(f"Double of 5: {double(5)}")
        print(f"Triple of 5: {triple(5)}")
        
        # Function that takes functions as arguments
        def apply_operations(value, operations):
            result = value
            for operation in operations:
                result = operation(result)
            return result
        
        operations = [
            lambda x: x + 10,
            lambda x: x * 2,
            lambda x: x - 5
        ]
        
        print(f"Result after applying operations to 5: {apply_operations(5, operations)}")

    def demo_closures(self) -> None:
        """Demonstrate closures"""
        def create_counter(start=0):
            count = [start]  # Using list for mutable state
            
            def increment(amount=1):
                count[0] += amount
                return count[0]
            
            def decrement(amount=1):
                count[0] -= amount
                return count[0]
            
            def get_count():
                return count[0]
            
            # Return a dictionary of functions that share the same count state
            return {
                'increment': increment,
                'decrement': decrement,
                'get_count': get_count
            }
        
        counter = create_counter(10)
        print(f"Initial count: {counter['get_count']()}")
        print(f"After increment: {counter['increment']()}")
        print(f"After incrementing by 5: {counter['increment'](5)}")
        print(f"After decrement: {counter['decrement']()}")

    # Error Handling and Context Managers
    def demo_error_handling(self) -> None:
        """Demonstrate error handling with try-except blocks"""
        # Basic try-except
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            print(f"Caught exception: {e}")
        
        # Multiple exception types
        try:
            num = int("not a number")
        except (ValueError, TypeError) as e:
            print(f"Caught value/type error: {e}")
        
        # try-except-else-finally
        try:
            result = 10 / 2
        except ZeroDivisionError:
            print("Division by zero!")
        else:
            print(f"Division successful, result: {result}")
        finally:
            print("This always executes")
        
        # Custom exception
        class NegativeNumberError(Exception):
            def __init__(self, value):
                self.value = value
                self.message = f"Negative numbers not allowed: {value}"
                super().__init__(self.message)
        
        def process_positive_number(n):
            if n < 0:
                raise NegativeNumberError(n)
            return n * 2
        
        try:
            print(process_positive_number(-5))
        except NegativeNumberError as e:
            print(f"Caught custom exception: {e}")

    def demo_context_managers(self) -> None:
        """Demonstrate context managers (with statement)"""
        # Using built-in context manager
        # Creating a temporary file for demonstration
        tmp_filename = "temp_demo_file.txt"
        
        # Using with statement with a file
        with open(tmp_filename, 'w') as f:
            f.write("Hello, context managers!")
        
        print(f"File written using context manager")
        
        # Custom context manager using class
        class Timer:
            def __enter__(self):
                self.start = time.time()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                self.end = time.time()
                print(f"Time elapsed: {self.end - self.start:.6f} seconds")
                return False  # Don't suppress exceptions
        
        with Timer():
            time.sleep(0.1)
            print("Doing some work...")
        
        # Custom context manager using contextlib
        @contextlib.contextmanager
        def temp_directory(dir_name):
            print(f"Would create directory {dir_name}")
            try:
                # Would normally create the directory here
                yield dir_name
            finally:
                print(f"Would remove directory {dir_name}")
        
        with temp_directory("demo_dir") as dir:
            print(f"Working in {dir}")
        
        # Clean up temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

    # Unpacking and Advanced Function Features
    def demo_unpacking(self) -> None:
        """Demonstrate unpacking operations"""
        # Unpacking lists and tuples
        a, b, c = [1, 2, 3]
        print(f"Unpacked list: a={a}, b={b}, c={c}")
        
        # Extended unpacking with *
        first, *middle, last = [1, 2, 3, 4, 5]
        print(f"Extended unpacking: first={first}, middle={middle}, last={last}")
        
        # Unpacking in function calls
        def add_three(x, y, z):
            return x + y + z
        
        numbers = [1, 2, 3]
        print(f"Unpacking in function call: {add_three(*numbers)}")
        
        # Dictionary unpacking
        person = {'name': 'Alice', 'age': 30, 'city': 'New York'}
        print("Unpacked dictionary:", end=" ")
        for k, v in person.items():
            print(f"{k}={v}", end=" ")
        print()
        
        # Merging dictionaries with **
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'c': 3, 'd': 4}
        merged = {**dict1, **dict2}
        print(f"Merged dictionaries: {merged}")

    def demo_functional_tools(self) -> None:
        """Demonstrate functional programming tools"""
        # Using map
        numbers = [1, 2, 3, 4, 5]
        squares = list(map(lambda x: x**2, numbers))
        print(f"Map result: {squares}")
        
        # Using filter
        evens = list(filter(lambda x: x % 2 == 0, numbers))
        print(f"Filter result: {evens}")
        
        # Using reduce
        product = functools.reduce(lambda x, y: x * y, numbers)
        print(f"Reduce result (product): {product}")
        
        # Using itertools
        permutations = list(itertools.permutations([1, 2, 3], 2))
        print(f"Permutations of [1, 2, 3] taken 2 at a time: {permutations}")
        
        combinations = list(itertools.combinations([1, 2, 3, 4], 2))
        print(f"Combinations of [1, 2, 3, 4] taken 2 at a time: {combinations}")
        
        # Chaining iterators
        chained = list(itertools.chain([1, 2], [3, 4], [5, 6]))
        print(f"Chained iterables: {chained}")

    def demo_advanced_functions(self) -> None:
        """Demonstrate advanced function features"""
        # Function with default arguments
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"
        
        print(greet("Python"))
        print(greet("Python", "Welcome"))
        
        # Function with *args
        def sum_all(*args):
            return sum(args)
        
        print(f"Sum of 1, 2, 3: {sum_all(1, 2, 3)}")
        print(f"Sum of 1 to 5: {sum_all(1, 2, 3, 4, 5)}")
        
        # Function with **kwargs
        def create_person(**kwargs):
            person = kwargs.copy()
            person.setdefault('species', 'Human')  # Default value if not provided
            return person
        
        print(f"Person 1: {create_person(name='Alice', age=30)}")
        print(f"Person 2: {create_person(name='Bob', age=25, job='Developer')}")
        
        # Function with all parameter types
        def display_info(required, *args, optional="default", **kwargs):
            return {
                'required': required,
                'args': args,
                'optional': optional,
                'kwargs': kwargs
            }
        
        print(f"Function with all parameter types: {display_info('hello', 1, 2, 3, optional='custom', x=10, y=20)}")

    # Regular Expressions
    def demo_regular_expressions(self) -> None:
        """Demonstrate regular expressions"""
        # Basic pattern matching
        text = "The quick brown fox jumps over the lazy dog"
        pattern = r"fox"
        match = re.search(pattern, text)
        print(f"Found '{pattern}' at position {match.start() if match else 'not found'}")
        
        # Using regex with groups
        email_pattern = r"([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})"
        email = "user.name@example.com"
        match = re.match(email_pattern, email)
        if match:
            print(f"Email parts: Username='{match.group(1)}', Domain='{match.group(2)}', TLD='{match.group(3)}'")
        
        # Finding all matches
        text = "Contacts: alice@example.com, bob@gmail.com, charlie@company.org"
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        print(f"All emails found: {emails}")
        
        # Substitution
        censored = re.sub(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", "[EMAIL REDACTED]", text)
        print(f"After substitution: {censored}")
        
        # Using regex flags
        case_insensitive = re.findall(r"fox", text, re.IGNORECASE)
        print(f"Case-insensitive search for 'fox': {case_insensitive}")

    # Collections Module
    def demo_collections_module(self) -> None:
        """Demonstrate data structures from the collections module"""
        # Counter
        text = "mississippi"
        counter = collections.Counter(text)
        print(f"Character frequency in '{text}': {counter}")
        print(f"Most common 2 characters: {counter.most_common(2)}")
        
        # defaultdict
        grouped_words = collections.defaultdict(list)
        words = ["apple", "bat", "apple", "car", "bat", "dog", "apple"]
        for word in words:
            grouped_words[len(word)].append(word)
        
        print(f"Words grouped by length: {dict(grouped_words)}")
        
        # OrderedDict
        ordered = collections.OrderedDict()
        ordered['first'] = 1
        ordered['second'] = 2
        ordered['third'] = 3
        print(f"OrderedDict items: {list(ordered.items())}")
        
        # namedtuple
        Person = collections.namedtuple('Person', ['name', 'age', 'job'])
        alice = Person('Alice', 30, 'Engineer')
        print(f"namedtuple: {alice}")
        print(f"Accessing fields: name={alice.name}, age={alice.age}")
        
        # deque (double-ended queue)
        dq = collections.deque([1, 2, 3])
        dq.append(4)  # Add to right
        dq.appendleft(0)  # Add to left
        print(f"Deque after operations: {dq}")
        print(f"Pop from right: {dq.pop()}, resulting deque: {dq}")
        print(f"Pop from left: {dq.popleft()}, resulting deque: {dq}")

    # Threading and Concurrency
    def demo_threading(self) -> None:
        """Demonstrate threading and concurrency"""
        # Basic threading
        def worker(name, delay):
            print(f"Worker {name} starting")
            time.sleep(delay)
            print(f"Worker {name} finished")
        
        threads = []
        for i in range(3):
            t = threading.Thread(target=worker, args=(f"Thread-{i}", 0.2))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        print("All threads completed")
        
        # Using ThreadPoolExecutor
        print("Using ThreadPoolExecutor:")
        def task(n):
            time.sleep(0.1)
            return n * n
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(task, i) for i in range(1, 6)]
            
            for future in concurrent.futures.as_completed(futures):
                print(f"Task result: {future.result()}")

    # Type Hints
    def demo_type_hints(self) -> None:
        """Demonstrate type hints"""
        def add_numbers(a: int, b: int) -> int:
            return a + b
        
        print(f"Add numbers: {add_numbers(5, 10)}")
        
        def process_items(items: List[str]) -> Dict[str, int]:
            return {item: len(item) for item in items}
        
        print(f"Process items: {process_items(['apple', 'banana', 'cherry'])}")
        
        # Function with optional parameters
        def greet_user(name: str, age: Optional[int] = None) -> str:
            if age is None:
                return f"Hello, {name}!"
            return f"Hello, {name}! You are {age} years old."
        
        print(greet_user("Alice"))
        print(greet_user("Bob", 25))
        
        # Function with Union type
        def process_input(value: Union[str, int]) -> str:
            if isinstance(value, int):
                return f"Received number: {value}"
            return f"Received string: {value}"
        
        print(process_input(42))
        print(process_input("Hello"))
        
        # Function with callable parameter
        def apply_twice(func: Callable[[int], int], value: int) -> int:
            return func(func(value))
        
        print(f"Apply twice (double): {apply_twice(lambda x: x * 2, 3)}")
        print(f"Apply twice (increment): {apply_twice(lambda x: x + 1, 5)}")


# Run the demonstration
if __name__ == "__main__":
    showcase = PythonConceptsShowcase()
    showcase.run_all_demos()
