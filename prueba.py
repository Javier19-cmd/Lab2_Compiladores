from reg import evaluar

class Node:
    def __init__(self, op=None, label=None, left=None, right=None, child=None):
        self.op = op
        self.label = label
        self.left = left
        self.right = right
        self.hijo = child

    def __str__(self):
        if self.op == "|":
            return f"{self.left}|{self.right}"
        elif self.op == ".":
            return f"{self.left}.{self.right}"
        elif self.op == "*":
            return f"{self.hijo}*"
        else:
            return self.label

def thompson(regex):
    stack = []

    for char in regex:
        if char == "|":
            right = stack.pop()
            left = stack.pop()
            node = Node(op="|", left=left, right=right)
            stack.append(node)
        elif char == ".":
            right = stack.pop()
            left = stack.pop()
            node = Node(op=".", left=left, right=right)
            stack.append(node)
        elif char == "*":
            hijo = stack.pop()
            node = Node(op="*", child=hijo)
            stack.append(node)
        else:
            node = Node(label=char)
            stack.append(node)

    return stack.pop()

e = evaluar("ab|c*")

print(thompson(e))