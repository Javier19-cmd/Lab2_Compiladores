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

    def __str__(self):
        return str(self.label)

    # def __str__(self): # Imprimiendo el árbol.
    #     # Impriendo el árbol en preorden.
    #     return str(self.left) + str(self.label) + str(self.right)