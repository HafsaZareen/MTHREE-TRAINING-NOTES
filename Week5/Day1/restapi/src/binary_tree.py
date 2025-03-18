class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value into the binary tree (level order)."""
        new_node = TreeNode(value)
        if not self.root:
            self.root = new_node
            return

        queue = [self.root]
        while queue:
            temp = queue.pop(0)

            if not temp.left:
                temp.left = new_node
                return
            else:
                queue.append(temp.left)

            if not temp.right:
                temp.right = new_node
                return
            else:
                queue.append(temp.right)

    def search(self, value):
        """Search for a value in the tree."""
        if not self.root:
            return False
        
        queue = [self.root]
        while queue:
            temp = queue.pop(0)
            if temp.value == value:
                return True
            
            if temp.left:
                queue.append(temp.left)
            if temp.right:
                queue.append(temp.right)
        
        return False

    def delete(self, value):
        """Delete a node from the binary tree."""
        if not self.root:
            return

        queue = [self.root]
        key_node = None
        last_node = None
        parent_of_last = None

        while queue:
            temp = queue.pop(0)

            if temp.value == value:
                key_node = temp  # Node to delete

            if temp.left:
                parent_of_last = temp
                last_node = temp.left
                queue.append(temp.left)
            if temp.right:
                parent_of_last = temp
                last_node = temp.right
                queue.append(temp.right)

        if key_node:
            key_node.value = last_node.value  # Replace value
            if parent_of_last.right == last_node:
                parent_of_last.right = None
            else:
                parent_of_last.left = None

    def inorder_traversal(self, node):
        """Inorder traversal: Left -> Root -> Right."""
        if node:
            self.inorder_traversal(node.left)
            print(node.value, end=" ")
            self.inorder_traversal(node.right)

    def preorder_traversal(self, node):
        """Preorder traversal: Root -> Left -> Right."""
        if node:
            print(node.value, end=" ")
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)

    def postorder_traversal(self, node):
        """Postorder traversal: Left -> Right -> Root."""
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.value, end=" ")

