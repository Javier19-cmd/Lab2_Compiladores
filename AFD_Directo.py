"""
Clase para la conversión de un regex a AFD.
"""
from Arbol import Tree

class AFD_Directo:

    def __init__(self, regex): # Se recibe la expresión regular para luego convertirla a AFD.
        self.regex = regex

        self.aumento() # Se le agrega un # al final de la expresión regular.
        print("La expresion regular es: ", self.regex)

        resultado = self.arbol() # Construyendo el árbol.

        self.const(resultado) # Construyendo el AFD.

    def aumento(self): # Función para agregarle un # al final de la expresión regular.
        self.regex = self.regex + "#."

    # Funciones para construir el árbol de la expresión regular.
    def anulable(self, regex):
        if regex == "ε":
            return True
        elif regex == "#":
            return False
        elif regex == ".":
            return self.anulable(regex[0]) and self.anulable(regex[1])
        elif regex == "|":
            return self.anulable(regex[0]) or self.anulable(regex[1])
        elif regex == "*":
            return True
        else:
            return False
    
    # Función para obtener la primera posición de la expresión regular.
    def primeraPosicion(self, regex):
        if regex == "ε":
            return set()
        elif regex == "#":
            return set()
        elif regex == ".":
            if self.anulable(regex[0]):
                return self.primeraPosicion(regex[0]) | self.primeraPosicion(regex[1])
            else:
                return self.primeraPosicion(regex[0])
        elif regex == "|":
            return self.primeraPosicion(regex[0]) | self.primeraPosicion(regex[1])
        elif regex == "*":
            return self.primeraPosicion(regex[0])
        else:
            return {regex}
    
    # Función para obtener la última posición de la expresión regular.
    def ultimaPosicion(self, regex):
        if regex == "ε":
            return set()
        elif regex == "#":
            return set()
        elif regex == ".":
            if self.anulable(regex[1]):
                return self.ultimaPosicion(regex[0]) | self.ultimaPosicion(regex[1])
            else:
                return self.ultimaPosicion(regex[1])
        elif regex == "|":
            return self.ultimaPosicion(regex[0]) | self.ultimaPosicion(regex[1])
        elif regex == "*":
            return self.ultimaPosicion(regex[0])
        else:
            return {regex}
    
    # Función para obtener la posición siguiente de la expresión regular.
    def siguientePosicion(self, regex):
        # Si la regex es un punto con hijo izquierdo c1 e hijo derecho c2, entonces para cada posición de c1, todas las posiciones de c2 se encuentran en última posición.
        if regex == ".":
            # Por cada última posición de c1, todas las posiciones de c2 se encuentran en última posición.
            ultimasPosicioness = self.ultimaPosicion(regex[0])

            # Encontrando las primeras posiciones de c2.
            primerasPosiciones = self.primeraPosicion(regex[1])

            # Creando un diccionario para guardar las posiciones.
            diccionario = {}

            # Recorriendo las últimas posiciones de c1.
            for ultimaPosicion in ultimasPosicioness:
                # Recorriendo las primeras posiciones de c2.
                for primeraPosicion in primerasPosiciones:
                    # Si la última posición de c1 es igual a la primera posición de c2, se guarda en el diccionario.
                    if ultimaPosicion == primeraPosicion:
                        diccionario[ultimaPosicion] = primeraPosicion

            # Retornando el diccionario.
            return diccionario
        
        # Si la regex es un * con un hijo c, todas las posiciones de c se encuentran en cada última posición de c.
        elif regex == "*":
            # Encontrando las últimas posiciones c de las primeras posiciones de c.
            ultimasPosiciones = self.ultimaPosicion(regex[0])

            return self.siguientePosicion(regex[0]) | ultimasPosiciones
        
    def arbol(self): # Función para construir el AFD. 
        # Paso 1 - Armar el árbol de la expresión regular.

        stack = [] # Pila para guardar los nodos del árbol.

        diccionario = {} # Diccionario para guardar las posiciones de cada nodo.

        # Recorriendo la expresión regular.
        for c in self.regex:
            if c == "|": # Si el caracter es un or, entonces se crea un nodo con el caracter y se agregan los dos últimos nodos de la pila como hijos.
                dereha1 = stack.pop()
                izquierda1 = stack.pop()

                nodo = Tree(op=c, left=izquierda1, right=dereha1)

                stack.append(nodo)

                # print("Izquierda del nodo del or: ", nodo.left)
                # print("Derecha del nodo del or: ", nodo.right)
                #print("Operación del or: ", nodo.op)

                # print("El nodo es: ", nodo)

                #print("Nodo: ", str(nodo))
            
            elif c == ".": # Si el caracter es un punto, entonces se crea un nodo con el caracter y se agregan los dos últimos nodos de la pila como hijos.
                dereha2 = stack.pop()
                izquierda2 = stack.pop()
                
                nodo2 = Tree(op=c, left=izquierda2, right=dereha2)

                #print("Izquierda del nodo del punto: ", nodo2.left)

                stack.append(nodo2)

                # print("Izquierda del nodo: ", nodo2.left)
                # print("Derecha del nodo: ", nodo2.right)
                # print("Operación: ", nodo2.op)

                #print("Nodo: ", str(nodo2))
            
            elif c == "*": # Si el caracter es un asterisco, entonces se crea un nodo con el caracter y se agrega el último nodo de la pila como hijo.
                hijo = stack.pop()

                #print("Hijo del nodo en el kleene: ", hijo)

                nodo3 = Tree(op=c, child=hijo)

                stack.append(nodo3)

                # print("Hijo del nodo: ", nodo3.child)
                # print("Operación: ", nodo3.op)

                # print("El nodo es: ", nodo3)

                #print("Nodo: ", str(nodo3))
            
            else: # Si el caracter no es un operador, entonces se crea un nodo con el caracter.
                nodo4 = Tree(label=c)

                stack.append(nodo4)

                #print("Label del nodo: ", nodo4.label)

                #print("Nodo: ", str(nodo4))
    

        return stack.pop() # Retornando el árbol.
    
    def const(self, arbol): # Método para construir el AFD.

        print("Árbol: ", arbol)

        for nodo in arbol: # Imprimiendo el árbol para ver sus nodos y padres.
            if nodo != None:
                print("Nodo: ", nodo)

        

        