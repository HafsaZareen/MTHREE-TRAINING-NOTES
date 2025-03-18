# #Code a stack prompem to cover all concepst of stack and its appication
# import math
# class Stack:
#     def __init__(self):
#         self.items = []

#     def is_empty(self):
#         return len(self.items) == 0

#     def push(self, item):
#         self.items.append(item)

#     def pop(self):
#         return self.items.pop()

#     def peek(self):
#         return self.items[-1]

#     def size(self):
#         return len(self.items)

#     def __str__(self):
#         return str(self.items)

#     def __repr__(self):
#         return repr(self.items)

#     def __len__(self):
#         return len(self.items)

#     def __contains__(self, item):
#         return item in self.items

#     def __getitem__(self, index):
#         return self.items[index]

#     def __setitem__(self, index, value):
#         self.items[index] = value

#     def __delitem__(self, index):
#         del self.items[index]

#     def __iter__(self):
#         return iter(self.items)

#     def __reversed__(self):
#         return reversed(self.items)

#     def __eq__(self, other):
#         return self.items == other.items

#     def __ne__(self, other):
#         return self.items != other.items

#     def __gt__(self, other):
#         return self.items > other.items

#     def __ge__(self, other):
#         return self.items >= other.items

#     def __lt__(self, other):
#         return self.items < other.items

#     def __le__(self, other):
#         return self.items <= other.items

#     def __hash__(self):
#         return hash(self.items)

#     def __add__(self, other):
#         return self.items + other.items

#     def __iadd__(self, other):
#         self.items += other.items

#     def __mul__(self, other):
#         return self.items * other.items

#     def __imul__(self, other):
#         self.items *= other.items

#     def __truediv__(self, other):
#         return self.items / other.items

#     def __itruediv__(self, other):
#         self.items /= other.items

#     def __floordiv__(self, other):
#         return self.items // other.items

#     def __ifloordiv__(self, other):
#         self.items //= other.items

#     def __mod__(self, other):
#         return self.items % other.items

#     def __imod__(self, other):
#         self.items %= other.items

#     def __pow__(self, other):
#         return self.items ** other.items

#     def __ipow__(self, other):
#         self.items **= other.items

#     def __neg__(self):
#         return -self.items

#     def __pos__(self):
#         return +self.items

#     def __abs__(self):
#         return abs(self.items)

#     def __round__(self, n=None):
#         return round(self.items, n)

#     def __ceil__(self):
#         return math.ceil(self.items)

#     def __floor__(self):
#         return math.floor(self.items)

# if __name__ == "__main__":
#     stack = Stack()
#     stack.push(1)
#     stack.push(2)
#     stack.push(3)
#     print(stack)
#     print(stack.pop())
#     print(stack)
#     print(stack.peek())
#     print(stack.size())
#     print(stack.is_empty())
#     print(stack.items)
#     print(stack.items[0])
#     print(stack.items[-1])
#     print(stack.items[1:3])
#     print(stack.items[:3])
#     print(stack.items[1:])
#     print(stack.items[::2])
#     print(stack.items[::-1])
#     print(stack.items[::-2])
#     print(stack.items[::-3])
#     print(stack.items[::-4])
#     print(stack.items[::-5])
#     print(stack.items[::-6])
#     print(stack.items[::-7])
#     print(stack.items[::-8])
#     print(stack.items[::-9])

st=[1,2,3,4,5]
st2=[]

for i in st:
    st2.append(i)

print(st2)


