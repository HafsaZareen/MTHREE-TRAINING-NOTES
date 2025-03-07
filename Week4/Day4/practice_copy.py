import copy
class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
    def __repr__(self):
        return f"Person(name={self.name}, address={self.address})"
class Address:
    def __init__(self, city, country):
        self.city = city
        self.country = country
        
    def __repr__(self):
        return f"Address(city={self.city}, country={self.country})"

# Create a person with an address
address = Address("New York", "USA")
# person = Person("John", address)
person = Person("John",address)


# Create a shallow copy
shallow_person = copy.copy(person)

# Create a deep copy
deep_person = copy.deepcopy(person)

# Verify the objects are different
# print(f"Original address ID: {id(address)}")
print(f"Original person ID: {id(person)}")
print(f"Shallow copy person ID: {id(shallow_person)}")
#shallow copy persion id and original person id are different because in shallow copy, the address is the same object
print(f"Deep copy person ID: {id(deep_person)}")

# But the address in the shallow copy is the same object
print(f"Original address ID: {id(person.address)}")
print(f"Shallow copy address ID: {id(shallow_person.address)}")
print(f"Deep copy address ID: {id(deep_person.address)}")

# Now change the original address
person.address.city = "Boston"

# Check all objects
print(f"Original person: {person}")
print(f"Shallow copy person: {shallow_person}")  # The city will be Boston
print(f"Deep copy person: {deep_person}")        # The city will still be New York

# The key difference with a shallow copy is how it handles nested objects (like the Address object within the Person).
# Instead of creating a new Address object, the shallow copy simply copies the reference to the original Address object.
# This is why person.address and shallow_person.address have the same ID.

