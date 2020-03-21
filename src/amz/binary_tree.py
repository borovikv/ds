from typing import List


class Node:
    def __init__(self, value):
        self.value = value
        self.left: Node = None
        self.right: Node = None

    def add(self, node):
        if node >= self:
            if self.right is None:
                self.right = node
            else:
                self.right.add(node)
        else:
            if self.left is None:
                self.left = node
            else:
                self.left.add(node)

    def __ge__(self, other):
        return self.value >= other.value

    def to_str(self, level=1):
        result = str(self.value) if level == 1 else ''
        for child in self.children:
            result += '\n' + '\t' * level + str(child.value)
            result += child.to_str(level=level + 1)
        return result

    @property
    def children(self) -> List["Node"]:
        return list(filter(bool, [self.left, self.right]))

    def __str__(self):
        return self.to_str()


root = Node(3)
root.add(Node(2))
root.add(Node(5))
root.add(Node(1))
root.add(Node(4))
root.add(Node(6))
root.add(Node(7))
root.add(Node(8))
root.add(Node(9))
root.add(Node(3))

print(root)


def tree_length(root: Node, length=0):
    return length if not root.children else max(tree_length(c, length=length + 1) for c in root.children)


print(tree_length(root))
