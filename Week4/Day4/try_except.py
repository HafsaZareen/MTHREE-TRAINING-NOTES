#Try except finally with detail example of all exeptions i would cover that
class CustomException(Exception):
    def _init_(self, message):
        self.message = message
        super()._init_(self.message)

try:
    raise CustomException("This is a custom exception")
except CustomException as e:
    print(e)
except Exception as e:
    print(e)
finally:
    print("Finally block")