#Try except finally with detail example of all exeptions i would cover that
class CustomException(Exception):
    def __init__(self, message):
        self.message = message
        # super().__init__(self.message)
        #is used to call the parent class's (Exception) constructor and pass the error message to it. 
try:
    # Uncomment one of the following lines at a time to see different exceptions
    
    # 1. ZeroDivisionError
    # result = 10 / 0  

    # 2. ValueError
    # num = int("abc")  

    # 3. IndexError
    # lst = [1, 2, 3]
    # print(lst[5])  

    # 4. KeyError
    # d = {"name": "Alice"}
    # print(d["age"])  

    # 5. FileNotFoundError
    # with open("non_existent_file.txt", "r") as f:
    #     content = f.read()  

    # 6. TypeError
    # result = "string" + 10  

    # 7. NameError
    # print(undefined_variable)  

    # 8. Custom Exception
    raise CustomException("This is a custom exception")  

except ZeroDivisionError as e:
    print("Error: Division by zero is not allowed.",e)

except ValueError as e:
    print("Error: Invalid input. Cannot convert to an integer.",e)

except IndexError as e:
    print("Error: List index out of range.",e)

except KeyError as e:
    print("Error: Key not found in dictionary.",e)

except FileNotFoundError as e:
    print("Error: The specified file does not exist.",e)

except TypeError as e:
    print("Error: Type mismatch in operations.",e)

except NameError as e:
    print("Error: Undefined variable used.",e)

except CustomException as e:
        print(f"Caught CustomException: {e}")

except Exception as e:
    print(f"Caught General Exception: {e}")

finally:
    print("Finally block executed.")
