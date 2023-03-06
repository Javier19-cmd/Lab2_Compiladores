"""
Clase para la conversión de un regex a AFD.
"""
from NodoA import *
from EstadoAFD import *
import graphviz as gv

class SintaxT:

    def __init__(self, regex, alfabeth): # Se recibe la expresión regular para luego convertirla a AFD.
        self.regex = regex
        self.alfabeth = alfabeth
        self.contador = 1 # Contador de los estados.
        self.followpos = [] # Lista para guardar los followpos.
        self.leaves = dict()
        self.estadosAFD = [] # Lista con los estados a utilizar.
        self.estadosAFD_dict = [] # Diccionario para graficar.
        self.terminal = None

        self.aumento() # Se le agrega un # al final de la expresión regular.
        #print("La expresion regular es: ", self.regex)

        self.tarbol = self.arbol() # Construyendo el árbol.

        self.tree = self.analisis(self.tarbol) # Construyendo el AFD.

        self.construir() # Construyendo el árbol.

        self.grafica() # Método para graficar.

    def aumento(self): 
        # Paso 1 - Aumentar el árbol para obtener el AFD.

        self.regex = self.regex + "#."
        

    # Función anulable para cada nodo el árbol.
    def anulable(self, regex):
        if regex.etiqueta == "ε":
            return True
        elif regex.etiqueta == ".":
            return self.anulable(regex.left) and self.anulable(regex.right)
        elif regex.etiqueta == "|":
            return self.anulable(regex.left) or self.anulable(regex.right)
        elif regex.etiqueta == "*":
            return True
        elif regex.etiqueta not in ["|", ".", "*"]:
            return False
            
        
    def arbol(self): # Función para construir el AFD. 
        # Paso 2 - Armar el árbol de la expresión regular.

        stack = []

        resultado = []

        #print("Expresión regular: ", self.regex)

        operaciones = ["|", ".", "*"]

        for c in self.regex:

            if c not in operaciones: # Carateres del regex.
                #print("Caracter: ", c)
                nodo1 = NodoA(etiqueta=c)

                #print("Nodo creado: ", nodo1, "Caracter: ", nodo1.etiqueta)

                stack.append(nodo1)

                resultado.append(nodo1)

            elif c == ".": # Concatenación.
                derecha1 = stack.pop()
                izquierda1 = stack.pop()

                nodo2 = NodoA(etiqueta=c, left=izquierda1, right=derecha1)

                # print("Derecha1: ", derecha1)
                # print("Izquierda1: ", izquierda1)

                #print("Nodo creado: ", nodo2)
                #print("Etiqueta: ", nodo2.etiqueta, "Izquierda: ", nodo2.left, "Derecha: ", nodo2.right)

                stack.append(nodo2)

                resultado.append(nodo2)

            elif c == "|":

                derecha2 = stack.pop()
                izquierda2 = stack.pop()

                # print("Derecha2: ", derecha2)
                # print("Izquierda2: ", izquierda2)

                nodo3 = NodoA(etiqueta=c, left=izquierda2, right=derecha2)

                #print("Nodo creado: ", nodo3)
                #print("Etiqueta: ", nodo3.etiqueta, "Izquierda: ", nodo3.left, "Derecha: ", nodo3.right)

                stack.append(nodo3)

                resultado.append(nodo3)
            
            elif c == "*":

                hijo = stack.pop()

                # print("")

                nodo4 = NodoA(etiqueta=c, child=hijo)

                #print("Nodo creado: ", nodo4)
                #print("Etiqueta: ", nodo4.etiqueta, "hijo: ", nodo4.child)

                stack.append(nodo4)

                resultado.append(nodo4)


        return resultado
    
    # Función para obtener la posición siguiente de la expresión regular.
    def siguientePosicion(self, n):
    
        if n.etiqueta == ".": # Followpos del punto.
            for i in n.left.lastP:
                self.followpos[i] = self.followpos[i].union(n.right.firstP)
        
        if n.etiqueta == "*": # Followpos del kleene.
            for i in n.child.lastP:
                self.followpos[i] = self.followpos[i].union(n.child.firstP)
    
    def primeraPosicion(self, b):
        if b.etiqueta == "ε":
            pass
        elif b.etiqueta == ".":
            
            if b.left.Null:
                b.firstP = b.left.firstP.union(b.right.firstP)
            else:
                b.firstP = b.left.firstP
        
        
        elif b.etiqueta == "|":

            b.firstP = b.child.firstP
        
        elif b.etiqueta == "*":
        
            b.firstP = b.child.firstP
        
        elif b.etiqueta not in ["|", ".", "*"]:
            
            b.firstP.add(b.id)
    
    def ultimaPosicion(self, b):
        if b.etiqueta == "ε":
            pass
        elif b.etiqueta == ".":
            
            if b.right.Null:
                    b.lastP = b.left.lastP.union(b.right.lastP)
            else:
                b.lastP = b.right.lastP

        elif b.etiqueta == "|":
            
            b.lastP = b.child.lastP

        elif b.etiqueta == "*":
            
            b.lastP = b.child.lastP

        elif b.etiqueta not in ["|", ".", "*"]:
            
            b.lastP.add(b.id)
    
    def analisis(self, arbol): # Función para analizar el AFD.
        # Paso 3 - Analizar el AFD.

        #print("Árbol: ", arbol)

        diccionario = {} # Diccionario del árbol.


        # Identificando el root, que es el último punto después del #.
        # Recorriendo al revés el árbol.
        for i in range(len(arbol)-1, -1, -1):
            if arbol[i].etiqueta == ".":
                arbol[i].raiz = True
                break
        
        # # Imprimiendo cada nodo del árbol.
        # for ele in arbol: 
        #     print("Elemento: ", ele, "Raíz: ", ele.raiz)


        # Identificando los padres e hijos del árbol.
        for c in arbol:
            if c.etiqueta == "|":
                diccionario[c] = [c.left, c.right]

            elif c.etiqueta == ".":
                diccionario[c] = [c.left, c.right]
            
            elif c.etiqueta == "*":
                diccionario[c] = [c.child]
            
        # Colocándole un id a cada caracter del árbol.
        for c in arbol:
            if c.etiqueta not in ["|", ".", "*"]:
                c.id = self.contador
                self.contador += 1

            # if c.id is not None: 
            #     print("Id: ", c.id, "Caracter: ", c.etiqueta)
        
        self.followpos = [set() for i in range(self.contador)]

        # Colocando los valores de anulable.
        for a in arbol:
            a.Null = self.anulable(a)

        # Calculando el firstpos y el lastpos.
        for b in arbol:
            
            if b.etiqueta not in ["|", ".", "*"]:
                # b.firstP.add(b.id)
                # b.lastP.add(b.id)

                self.primeraPosicion(b)
                self.ultimaPosicion(b)

                # self.primeraPosicion(b)
                # self.ultimaPosicion(b)

                #print("Anulable: ", b.Null)
                # print("Label: ", b.etiqueta)
                # print("First pos: ", b.firstP)
                # print("Last pos: ", b.lastP)

            elif b.etiqueta == "|": # Computando el or.
                b.firstP = b.left.firstP.union(b.right.firstP)
                b.lastP = b.left.lastP.union(b.right.lastP)

                #print("Anulable: ", b.Null)
                # print("Or")
                # print("First pos: ", b.firstP)
                # print("Last pos: ", b.lastP)

            elif b.etiqueta == "*": # Computando el asterisco.

                #print("Kleene")
                b.firstP = b.child.firstP
                b.lastP = b.child.lastP
                #print("Anulable: ", b.Null)

                # print("Firstpos del *", b.firstP)
                # print("Lastpos del *", b.lastP)

                # print("Firstpos del hijo: ", b.child.firstP)
                # print("Lastpos del hijo: ", b.child.lastP)
                
                self.siguientePosicion(b) # Haciendo el followpos.

                # print("First pos: ", b.firstP)
                # print("Last pos: ", b.lastP)
            
            elif b.etiqueta == ".": # Computando el punto.
            
                if b.left.Null:
                    b.firstP = b.left.firstP.union(b.right.firstP)
                else:
                    b.firstP = b.left.firstP
                
                if b.right.Null:
                    b.lastP = b.left.lastP.union(b.right.lastP)
                else:
                    b.lastP = b.right.lastP
                

                self.siguientePosicion(b) # Haciendo el followpos.

                #print("Anulable: ", b.Null)
                # print("First pos: ", b.firstP)
                # print("Last pos: ", b.lastP)
            # elif b.etiqueta == "#":
            #     b.firstP = set()
            #     b.lastP = set()

            #     #print("Anulable: ", b.Null)
            #     # print("First pos: ", b.firstP)
            #     # print("Last pos: ", b.lastP)
            
            elif b.etiqueta == "ε":
                pass
        

    
        #print("Followpos: ", self.followpos)

        #Eliminando el primer set del followpos.
        #self.followpos.pop(0)

        # Guardando cada letra con su id.
        for c in arbol:
            if c.etiqueta not in ["|", ".", "*"]:
                self.leaves[c.id] = c.etiqueta

        print("Leaves: ", self.leaves)

        #print("Followpos: ", self.followpos)

        return arbol
    
    
    def construir(self): # Método para construir el AFD.

        # Variables a utilizar.
        id_c = 0
        ter = [] # Lista para guardar el terminal.
        first_p = set()

        
        # Guardando el #.
        for i in range(len(self.tree)-1, -1, -1):
            if self.tree[i].etiqueta == "#":
                ter.append(self.tree[i].id)
                break
        
        self.terminal = ter.pop() # Terminal del árbol.


        # Paso 4 - Construir el AFD.

        # print("Árbl en la construcción: ", self.tree)
        # print("Alfabeto en la construcción: ", self.alfabeth)
        
        # Recorriendo el árbol para imprimir su raíz.
        for i in range(len(self.tree)-1, -1, -1):
            if self.tree[i].etiqueta == ".":
                # print("Raíz: ", self.tree[i])
                # print("Firstpos de la raíz: ", self.tree[i].firstP)
                for p in self.tree[i].firstP:
                    first_p.add(p)
                break
    

        # Creando el estado inicial.
        estado_inicial = Estado(alfabeto=self.alfabeth, id_list=first_p, id=id_c, terminal_id=self.terminal)

        #print("Estado inicial: ", estado_inicial)
        
        id_c += 1 # Aumentando en 1 el id del estado.

        self.estadosAFD.append(estado_inicial) # Guardando el estado inicial.

        queue = [estado_inicial] # Haciendo una cola con el estado inicial.
        
        #print("Followpos: ", self.followpos)

        while len(queue) > 0: # Buscando las transisicones a todos los estados.
            st = queue.pop(0)
            nuevo_estado = self.DTran(st, self.terminal)

            for s in nuevo_estado:
                estadoo = Estado(self.alfabeth, s, id_c, self.terminal)
                self.estadosAFD.append(estadoo)
                queue.append(estadoo)
                #print("Cola: ", queue)
                id_c += 1
            

    def DTran(self, estado, terminal): # Cálculo de las transiciones.

        nuevo_estado = []
        for i in estado.id_set: # Si el estado final está en el set, se continúa.
            if i == terminal:
                continue
            
            label = self.leaves[i] # Agarrando el label de cada hoja.
            #print(label)

            if estado.transitions[label] == {}: # Transiciones del estado.
                #print("Followpos sin la unión: ", self.followpos[i])

                #print("Label: ", label, estado.transitions[label], "Su followpos: ", self.followpos[i])
                estado.transitions[label] = self.followpos[i]
            
            else: # Si las transiciones están llenas, entonces se unen los estados.
                #print("Followpos en la unión: ", self.followpos[i])
                estado.transitions[label] = estado.transitions[label].union(self.followpos[i])
            
        for a in self.alfabeth: # Transiciones con los símbolos.
            if estado.transitions[a] != {}:
                nuevo = True
                for e in self.estadosAFD:
                    if (e.id_set == estado.transitions[a]) or (estado.transitions[a] in nuevo_estado):
                        #print(e.id_set, estado.transitions[a])
                        nuevo = False
                
                if nuevo:
                    #print("Transición a agregar: ", estado.transitions[a]) 
                    nuevo_estado.append(estado.transitions[a])
            
        return nuevo_estado
    
    def grafica(self): #Método para graficar.
        grafo = gv.Digraph(comment="AFD", format="png")

        for estado in self.estadosAFD:
            print("Estados en el método de gráfica: ", estado)


        """
        Pasando las transiciones de los estados a una lista de la siguiente forma: 

        estado - simbolo - estado

        """

        lista = []
        for estado in self.estadosAFD:
            for simbolo in self.alfabeth:
                if estado.transitions[simbolo] != {}:
                    lista.append([estado.id_set, simbolo, estado.transitions[simbolo]])
        
        #print("Lista: ", lista)

        lista2 = []

        # Convirtiendo los sets de la lista a una nueva lista de listas.
        for i in range(len(lista)):
            # Guardando las listas como lista-símbolo-lista.
            lista2.append([list(lista[i][0]), lista[i][1], list(lista[i][2])])

        print("Lista: ", lista2)

        num = 0

        # Pasando la lista a un diccionario.
        #diccionario_estados = {}

        # for i in self.estadosAFD:
        #     etiqueta = "q" + str(num)
        #     num += 1
        #     diccionario_estados[etiqueta] = i

        # for key, value in diccionario_estados.items():
        #     print(key, value)

        # Colocando los estados.
        for estado in self.estadosAFD:

            #print("Terminal: ", self.terminal)
            if self.terminal in estado.id_set:
                grafo.node(str(estado.id_set), shape="doublecircle")
            else:
                grafo.node(str(estado.id_set))
            
            # Agregando las transiciones.
            for simbolo in self.alfabeth:
                if estado.transitions[simbolo] != {}:
                    grafo.edge(str(estado.id_set), str(estado.transitions[simbolo]), label=simbolo)

        # Colocando el autómta de manera horizontal.
        grafo.graph_attr['rankdir'] = 'LR'

        grafo.render("AFD_Directo", view=True)
