class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


class AVL_Tree:

    def insert(self, root, key):
        """
        Recursive function to insert key in
        subtree rooted with node and returns
        new root of subtree.
        """

        # Step 1 - Perform normal BST
        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # Step 2 - Update the height of the
        # ancestor node
        self.update_height(root)

        # Step 3 - Get the balance factor
        balance = self.getBalance(root)

        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and key < root.left.val:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.val:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.val:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def update_height(self, root):
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

    def leftRotate(self, z):
        y = z.right
        z.right = y.left
        y.left = z

        self.update_height(z)
        self.update_height(y)

        # Return the new root
        return y

    def rightRotate(self, z):
        y = z.left
        z.left = y.right
        y.right = z

        self.update_height(z)
        self.update_height(y)

        # Return the new root
        return y

    @staticmethod
    def getHeight(root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root, indent=0):
        if not root:
            return
        indentation = '\t' * indent
        print(f"{indentation}{root.val} ")
        self.preOrder(root.left, indent + 1)
        self.preOrder(root.right, indent + 1)


myTree = AVL_Tree()
r = None
for key in [10, 20, 30, 40, 50, 25]:
    r = myTree.insert(r, key)
    myTree.preOrder(r)
"""
The constructed AVL Tree would be 
         30 
        / \ 
        20 40 
      /   \ \ 
     10   25 50
"""

"""
Алгоритм удаления вершины
Для простоты опишем рекурсивный алгоритм удаления. 
Если вершина — лист,
    то удалим её и вызовем балансировку всех её предков в порядке от родителя к корню.
    иначе найдём самую близкую по значению вершину в поддереве наибольшей высоты (правом или левом)
        и переместим её на место удаляемой вершины, при этом вызвав процедуру её удаления.
"""
