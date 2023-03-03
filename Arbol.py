"""
Clase árbol para convertir el regex a árbol sintáctico.
"""

class Tree: 

    def __init__(self, op=None, label=None, left=None, right=None, child=None): # Se recibe el dato para crear el nodo.
        self.op = op
        self.label = label
        self.left = left
        self.right = right
        self.child = child

    # def insert_left(self, data): # Función para insertar un nodo a la izquierda.
    #     if self.left == None:
    #         self.left = Tree(data)
    #     else:
    #         t = Tree(data)
    #         t.left = self.left
    #         self.left = t

    # def insert_right(self, data): # Función para insertar un nodo a la derecha.
    #     if self.right == None:
    #         self.right = Tree(data)
    #     else:
    #         t = Tree(data)
    #         t.right = self.right
    #         self.right = t

    def get_left(self):
        return str(self.left)
    
    def get_right(self):
        return str(self.right)
    
    def get_child(self):
        return str(self.child)
    
    def get_op(self):
        return str(self.op)
    
    def get_label(self):
        return str(self.label)
    
    def __iter__(self):
        # yield self.op
        # yield self.label
        # yield self.left
        # yield self.right
        # yield self.child

        # # Devolviendo los nodos en preorden.
        # if self.left:
        #     yield from self.left
        # if self.right:
        #     yield from self.right
        # if self.child:
        #     yield from self.child
        
        # Devolviendo los nodos en preorden.
        if self.op == "|":
            yield from self.left
            yield from self.op
            yield from self.right
        elif self.op == ".":
            yield from self.left
            yield from self.op
            yield from self.right
        elif self.op == "*":
            yield from self.op
            yield from self.child
        else:
            yield self.label


    def __str__(self):
        if self.op == "|":
            return f"{self.left}|{self.right}"
        elif self.op == ".":
            return f"{self.left}.{self.right}"
        elif self.op == "*":
            return f"{self.child}*"
        else:
            return self.label

    # def __str__(self): # Imprimiendo el árbol.
    #     # Impriendo el árbol en preorden.
    #     return str(self.left) + str(self.label) + str(self.right)