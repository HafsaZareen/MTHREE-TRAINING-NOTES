# #Explain in detail the concepts  of a tree data structure inlcudeing root , node branches , tree
# #Then provide breakdown of common data traversal and search algorithms and the iimplementation using linkedlist
# #Then provide implementation of a binary search tree and its traversal algorithms
# #insertion , deletion , search , traversal

# class TreeNode:
#     def __init__(self, value):
#         self.value = value
#         self.children = []

#     def add_child(self, child):
#         self.children.append(child)

#     def remove_child(self, child):
#         self.children.remove(child)

#     def __str__(self):
#         return self.value   
    
#     def __repr__(self):
#         return f"TreeNode({self.value})"
    
#     def __len__(self):
#         return len(self.children)
    
#     def __contains__(self, value):
#         return value in self.children
    
#     def __getitem__(self, index):
#         return self.children[index]
    
#     def __setitem__(self, index, value):
#         self.children[index] = value
    
#     def __delitem__(self, index):
#         del self.children[index]
    
#     def __iter__(self):
#         return iter(self.children)
    
#     def __reversed__(self):
#         return reversed(self.children)
    
#     def __eq__(self, other):
#         return self.value == other.value
    
#     def __ne__(self, other):
#         return self.value != other.value
    
#     def __gt__(self, other):
#         return self.value > other.value
    
#     def __ge__(self, other):
#         return self.value >= other.value
    
#     def __lt__(self, other):
#         return self.value < other.value
    
#     def __le__(self, other):
#         return self.value <= other.value
    
#     def __hash__(self):
#         return hash(self.value)
    
#     def __bool__(self):
#         return bool(self.value)
    
#     def delete(self, str):
#         if str in self.children:
#             self.children.remove(str)
#         else:
#             for child in self.children:
#                 child.delete(str)

#     def inorder_traversal(self):
#         if self.children:
#             for child in self.children:
#                 child.inorder_traversal()
#         else:
#             print(self.value)
    
            
#     def __dir__(self):
#         return dir(self.value)
        
# if __name__ == "__main__":
#     tree = TreeNode("A")
#     tree.add_child("B")
#     tree.add_child("C")
#     tree.add_child("D")
#     tree.add_child("E")
#     tree.add_child("F")
#     tree.add_child("G")
#     tree.add_child("H")
#     tree.add_child("I")
#     tree.add_child("J")
#     tree.add_child("K")
#     tree.add_child("L")
#     tree.add_child("M")
#     tree.add_child("N")
#     tree.add_child("O")
#     tree.add_child("P")
#     tree.add_child("Q")
#     tree.add_child("R")
#     tree.add_child("S")
#     tree.add_child("T")
#     tree.add_child("U")
#     tree.add_child("V")
#     tree.add_child("W")
#     tree.add_child("X")
#     tree.add_child("Y")
#     tree.add_child("Z")
#     print(tree)
#     print(tree.children)
#     print(tree.children[0])
#     print(tree.children[1])
#     print(tree.children[0])
#     print(tree.children[1])

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def __str__(self):
        return self.value   
    
    def __repr__(self):
        return f"TreeNode({self.value})"
    
    def __len__(self):
        return len(self.children)
    
    def __contains__(self, value):
        return value in self.children
    
    def __getitem__(self, index):
        return self.children[index]
    
    def __setitem__(self, index, value):
        self.children[index] = value
    
    def __delitem__(self, index):
        del self.children[index]
    
    def __iter__(self):
        return iter(self.children)
    
    def __reversed__(self):
        return reversed(self.children)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __bool__(self):
        return bool(self.value)
    
    def delete(self, str):
        if str in self.children:
            self.children.remove(str)
        else:
            for child in self.children:
                child.delete(str)

    def inorder_traversal(self):
        if self.children:
            for child in self.children:
                child.inorder_traversal()
        else:
            print(self.value)
    
    def preorder_traversal(self):
        print(self.value)
        if self.children:
            for child in self.children:
                child.preorder_traversal()
    
    def postorder_traversal(self):
        if self.children:
            for child in self.children:
                child.postorder_traversal()
        else:
            print(self.value)
            
    def __dir__(self):
        return dir(self.value)
        
if __name__ == "__main__":
    tree = TreeNode("A")
    tree.add_child("B")
    tree.add_child("C")
    tree.add_child("D")
    tree.add_child("E")
    tree.add_child("F")
    tree.add_child("G")
    tree.add_child("H")
    tree.add_child("I")
    tree.add_child("J")
    tree.add_child("K")
    tree.add_child("L")
    tree.add_child("M")
    tree.add_child("N")
    tree.add_child("O")
    tree.add_child("P")
    tree.add_child("Q")
    tree.add_child("R")
    tree.add_child("S")
    tree.add_child("T")
    tree.add_child("U")
    tree.add_child("V")
    tree.add_child("W")
    tree.add_child("X")
    tree.add_child("Y")
    tree.add_child("Z")
    print(tree)
    # tree.inorder_traversal()
    # tree.preorder_traversal()
    # tree.postorder_traversal()
    print(tree.children)
    print(tree.children[0])
    print(tree.children[1])
    print(tree.children[0])
    print(tree.children[1].children)
    print(tree.children[0])
    print(tree.children[1])
    tree.delete("B")
    # tree.inorder_traversal()
    # tree.preorder_traversal()
    # tree.postorder_traversal()
