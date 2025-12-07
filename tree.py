class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def print_tree_recursive(node, level=0, result=None):
    if result is None:
        result = []
    result.append("  " * level + node.name)
    for child in node.children:
        print_tree_recursive(child, level + 1, result)
    return result
