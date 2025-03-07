class Resource:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
    def __str__(self):
        return f"Resource {self.name} has {self.quantity} units"
    def __del__(self):
        print(f"Resource {self.name} is being deleted")
    def set_age(self, age):
        self.age = age
    def get_age(self):
        return self.age
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
    def set_age_name(self, age, name):
        self.age = age
        self.name = name
    