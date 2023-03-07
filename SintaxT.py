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
        self.followposT = []
        self.leaves = dict()
        self.estadosAFD = [] # Lista con los estados a utilizar.
        self.EstadosAceptAFD = [] # Lista con los estados finales a utilizar.
        self.EstadoInicial = None # Estado inicial del AFD.
        self.transiciones = [] # Lista para guaradar las transiciones del AFD final.
        self.estadosAFD_dict = [] # Diccionario para graficar.
        self.terminal = None
        self.DTtrans = {}

        self.aumento() # Se le agrega un # al final de la expresión regular.
        #print("La expresion regular es: ", self.regex)

        self.tarbol = self.arbol() # Construyendo el árbol.

        self.tree = self.analisis(self.tarbol) # Construyendo el AFD.

        self.construir() # Construyendo el árbol.

        self.grafica() # Método para graficar.

        self.minimizar() # Minimización.

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

        #print("Leaves: ", self.leaves)

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

        # Guardando el estado inicial de forma global.
        self.EstadoInicial = estado_inicial

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
            
        # Guardando los estados finales en una lista.
        for e in self.estadosAFD:
            # Verificando que el id del estado final esté en el set.
            if self.terminal in e.id_set:
                self.EstadosAceptAFD.append(e)

        # Post processing.
        sin_estado = False
        for estado in self.estadosAFD:
            for a in self.alfabeth:
                if estado.transitions[a] == {}:
                    sin_estado = True
                    estado.transitions[a] == id_c
                
                SET = estado.transitions[a]
                for estado2 in self.estadosAFD:
                    if estado2.id_set == SET:
                        estado.transitions[a] = estado2.id
        
        # Imprimiendo las transiciones otra vez.
        for estado in self.estadosAFD:
            print("Estado con transiciones: ", estado.transitions)

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

        # for estado in self.estadosAFD:
        #     print("Estados en el método de gráfica: ", estado)

        # # Imprimiendo los estados y sus tansiciones.
        # for estado in self.estadosAFD:
        #     print("Estado: ", estado, "Transiciones: ", estado.transitions)
        
        # For indicado.
        for estado in self.estadosAFD:
            for a in self.alfabeth:
                
                trans = estado.transitions[a]
                print("Estado: ", estado, "Trans: ", trans)

                grafo.edge(str(estado), str(trans), label=a)

        # Dibujando los estados del AFD.
        for esta in self.estadosAFD:
            if esta in self.EstadosAceptAFD:
                print("Estado de aceptación: ", esta)
                grafo.node(str(esta), str(esta), shape="doublecircle")
            else:
                grafo.node(str(esta), str(esta), shape="circle")
        
        # Colocando el autómta de manera horizontal.
        grafo.graph_attr['rankdir'] = 'LR'

        grafo.render('AFD_Directo', view=True) # Dibujando el grafo.        
        

    # Haciendo la minimización.
    def minimizar(self):
        
        # # Imprimiendo las cosas que se van a utilizar.
        # for estado in self.estadosAFD:
        #     print("Estados en el método de minimización: ", estado)
        
        # for estadoAc in self.EstadosAceptAFD:
        #     print("Estados finales: ", estadoAc)

        # print("Estado inicial: ", self.EstadoInicial)

        # for alfabeto in self.alfabeth:
        #     print("Letra: ", alfabeto)
        
        # for transicion in self.transiciones:
        #     print("Transición: ", transicion)

        # Guardando los estados en una lista local.
        # for a in self.estadosAFD:
        #     print(a)

        
        # Paso 1: Creando una tabla de transiciones.
        tabla_trans = {state: {} for state in self.estadosAFD}

        # for a in tabla_trans: # Imprimiendo la tabla.
        #     print("Estado: ", a)


        diccionario = {}

        """
        Haciendo un diccionario con los estados y sus transiciones.
        """

        # for estado in self.estadosAFD:
        #     print("Estado: ", estado.transitions)

        # Creando un diccionario con el estado y sus transiciones.
        for estado in self.estadosAFD:
            for simbolo in self.alfabeth:
                if estado.transitions[simbolo] != {}:
                    if estado not in diccionario:
                        diccionario[estado] = {}

                    diccionario[estado][simbolo] = estado.transitions[simbolo]

        # for key, value in diccionario.items():
        #     print(key, value)

        Q = self.estadosAFD
        F = self.EstadosAceptAFD

        # División inicial de los estados.
        P = [self.EstadosAceptAFD, set(Q) - set(F)]
        W = [self.EstadosAceptAFD]

        while W: 
            A = W.pop()
            for a in self.alfabeth:
                X = []

                for q in A:
                    print("q: ", q)
                    X.append(diccionario[q][a])

                for el in X:
                    print("Estado: ", el)

                # for Y in P:
                #     Y_int_X = list(set(Y).intersection(set(X)))
                #     Y_minus_X = list(set(Y) - set(X))
                #     X_minus_Y = list(set(X) - set(Y))
                #     if Y_int_X and Y_minus_X:
                #         P.remove(Y)
                #         P.extend([Y_int_X, Y_minus_X])
                #         if Y in W:
                #             W.remove(Y)
                #             W.extend([Y_int_X, Y_minus_X])
                #         else:
                #             if len(Y_int_X) <= len(Y_minus_X):
                #                 W.append(Y_int_X)
                #             else:
                #                 W.append(Y_minus_X)
        
        
        # # Creación del autómata mínimo
        # Q_min = []
        # delta_min = {}
        # q0_min = None
        # F_min = []
        # for X in P:
        #     Q_min.append(X[0])
        #     delta_min[X[0]] = {}
        #     for a in self.alfabeth:
        #         for Y in P:
        #             if X[0] in Y:
        #                 delta_min[X[0]][a] = Y[0]
        #                 break
        # for X in P:
        #     if self.EstadoInicial in X:
        #         q0_min = X[0]
        #         break
        # for X in P:
        #     if set(X).intersection(set(self.EstadosAceptAFD)):
        #         F_min.append(X[0])
        
        
        # for elemento in self.transiciones: # Pasando las transiciones a un diccionario.
        #     if elemento[1] not in diccionario:
        #         diccionario[elemento[1]] = []

        #     diccionario[elemento[1]].append((elemento[0], elemento[2]))
    

        # for estado in self.estadosAFD:
        #     for simbolo in self.alfabeth:

        #         #print("Estado: ", estado, "Simbolo: ", simbolo, "Transiciones: ", diccionario[simbolo])

        #         tabla_trans[estado][simbolo] = diccionario[simbolo]

        
        # for key, value in tabla_trans.items():
        #     for transicion in value:
        #         print(key, transicion, value[transicion])

        # non_final_states = set(self.estadosAFD) - set(self.EstadosAceptAFD)
        # partitions = [self.EstadosAceptAFD, non_final_states]
        
        # # Repita hasta que no haya más conjuntos sin dividir
        # while True:
        #     new_partitions = []
        #     for partition in partitions:
        #         for symbol in self.alfabeth:
        #             # Dividir el conjunto según a qué estados van
        #             new_partition = []
        #             for state in partition:
        #                 next_state = tabla_trans[state][symbol]

        #                 print("Next state: ", next_state)

            #             for p in new_partition:
            #                 if next_state in p:
            #                     break
            #             else:
            #                 new_partition.append(set())
            #             new_partition[-1].add(state)
            #         new_partitions.extend(new_partition)
                
            # if new_partitions == partitions:
            #     break
            # else:
            #     partitions = new_partitions