class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []

    def add(self, node: 'Node'):
        node.parent = self
        self.children.append(node)
        return node

    def to_str(self, level=1):
        result = str(self.value) if level == 1 else ''
        for child in self.children:
            result += '\n' + '\t' * level + str(child.value)
            result += child.to_str(level=level + 1)
        return result

    def __repr__(self):
        return repr(self.value)


root = Node(1)
node = Node(5)
root.add(Node(2)).add(Node(3)).add(Node(4))
root.add(node)

print(root.to_str())


def path(root: Node, level=1):
    # print(root.value, root.children)
    result = []
    for child in root.children:
        result += [level * 6] + path(child, level + 1)
    return result


print(path(root))
