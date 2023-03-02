"""
Archivo que se encargará de convertir el autómata finito no determinista a un autómata finito determinista.
"""
from EstadoAFD import *
from TransicionesAFD import *
import graphviz as gv

class AFD:

    def __init__(self, alfabeto, automata, transiciones, diccionario):
        self.alfabeto = alfabeto
        self.automata = automata
        self.transiciones = transiciones
        self.diccionario = diccionario
        self.estado_num = 0
        self.trans_AFD = []
        self.estados_Finales = []
        self.estados_FinalesE = []
        self.estados_AFD = []
        self.estadoInicial = []
        self.dict = []

        self.conversion()
        self.graficar()

    def conversion(self): # Método para convertir el AFD a AFD.
        # Imprimiendo los datos del autómata.

        #print(self.automata)
        #print(self.diccionario)

        estado_inicial = self.eclosure(self.automata.estado_inicial) # Calculand el estado inicial del autómata.

        #print(estado_inicial) # Imprimiendo el estado inicial.

        estdos_AFD = [estado_inicial] # Creando la lista de estados_AFD y guardando su primer estado.
        
        #trans_AFD = [] # Creando la tabla de transición de los estados.

        estados_a_revisar = [estado_inicial] # Creando la lista de estados a revisar.

        #print("Estados a revisar: ", estados_a_revisar)

        while len(estados_a_revisar) > 0:
            estado_actual_AFD = estados_a_revisar.pop(0) # Sacando el último estado de la lista de estados a revisar.

            #print("Estado actual AFD: ", estado_actual_AFD)
            transiciones_act = {} # Transiciones actuales.

            for simbolo in self.alfabeto: # Recorriendo el alfabeto.


                # Lista para los estados alcanzables.
                estados_alcanzables = []

                # Recorriendo los estados del estado actual del AFD.
                for estado in estado_actual_AFD:
                        
                        # Verificando si el estado tiene transiciones con el símbolo actual.
                        if estado in self.diccionario:
                            
                            # Si tiene transiciones con el símbolo actual, se agregan a la lista de estados alcanzables.
                            for transicion in self.diccionario[estado]:
                                if transicion[0] == simbolo: # Imprimiendo las transiciones con el símbolo actual.
                                    # Calculando el cierre epsilon de los estados alcanzables.
                                    estadoo = self.eclosure(transicion[1])

                                    #print("Estadoo: ", estadoo)

                                    # Guardando los estados alcanzables.
                                    estados_alcanzables.append(estadoo)

                #print("Transiciones actuales: ", transiciones_act)
                
                if len(estados_alcanzables) > 0: 
                    for estad in estados_alcanzables: # Recorriendo los estados alcanzables y guardándolos en los estados del AFD.
                        if estad not in estdos_AFD:
                            estdos_AFD.append(estad)
                            estados_a_revisar.append(estad)
                    
                    # Guardando las transiciones actuales con el símbolo actual.
                    transiciones_act[simbolo] = estad

            #print("Estado actual: ", estado_actual_AFD, "transiciones: ", transiciones_act)

            #print("Estados AFD: ", estdos_AFD)

            # Recorriendo las transiciones actuales.
            for simboloo, estado_ll in transiciones_act.items():
                #print("Estado actual: ", estado_actual_AFD, "Simbolo: ", simboloo, "Estado: ", estado_ll)

                # Creando la transición del AFD.
                trans = TransicionesAFD(estado_actual_AFD, simboloo, estado_ll)

                self.trans_AFD.append(trans)


        
        #print("Transiciones del AFD: ", trans_AFD)

        # Creando un diccionario para guardar los estados con sus etiquetas.
        diccionario_estados = {}

        # Recorriendo los estados del AFD.
        for estado in estdos_AFD:
            #print("Estado: ", estado)

            # Dando una etiqueta al estado.
            etiqueta = "q" + str(self.estado_num)
            self.estado_num += 1

            # Guardando el estado con su etiqueta.
            diccionario_estados[etiqueta] = estado

        #print("Diccionario de estados: ", diccionario_estados)

        # Cambiando los estados del AFD por sus etiquetas en la tabla de transiciones.
        for transion in self.trans_AFD:
            for etiqueta, estado in diccionario_estados.items():
                if transion.estadoInicial == estado:
                    transion.estadoInicial = etiqueta
                
                if transion.estadoFinal == estado:
                    transion.estadoFinal = etiqueta


        #print("Transiciones: ", self.trans_AFD)
        
        # Identificando los estados finales del AFD.
        for estado in estdos_AFD:
            if self.automata.estado_final in estado:
                self.estados_Finales.append(estado)

        # Etiqutando los estados finales del AFD.
        for estadoss in self.estados_Finales:
            for etiqueta, estadso in diccionario_estados.items():
                if estadoss == estadso:
                    self.estados_FinalesE.append(etiqueta)

        # Guardando los estados etiquetados en una lista.
        for estado in estdos_AFD:
            for etiqueta, estad in diccionario_estados.items():
                if estado == estad:
                    self.estados_AFD.append(etiqueta)

        # Guardando el estado inicial del AFD.
        for estado in estdos_AFD:
            if estado == estado_inicial:
                # Buscando la etiqueta del estado inicial.
                for etiqueta, estadd in diccionario_estados.items():
                    if estado == estadd:
                        self.estado_inicial_AFD = etiqueta

        #return self.trans_AFD

    def eclosure(self, estado): #Método para calcular el cierre epsilon de un estado.
        
        # Lista para el resultado.
        resultado = []

        # Stack para realizar el procedimiento.
        pila = []

        # Pusheando el primer estado a la pila.
        pila.append(estado)

        while len(pila) > 0: 
            # Sacando el último elemento de la pila.
            estado = pila.pop()

            # Si el estado no está en el resultado, se agrega.
            if estado not in resultado:
                resultado.append(estado)

            # Verificando si el estado tiene transiciones epsilon.
            if estado in self.diccionario:
                # Si tiene transiciones epsilon, se agregan a la pila.
                for transicion in self.diccionario[estado]:
                    #print(transicion[0])

                    if transicion[0] == "ε":
                        #print("Sí hay transiciones epsilon.")
                        pila.append(transicion[1])


        # # Ordenando el resultado.
        # resultado.sort()
        
        #print("Resultado: ", resultado)

        # Retornando el resultado.
        return resultado
    
    def graficar(self): # Método para dibujar el AFD.
        
        grafo = gv.Digraph(comment="AFD", format="png") # Creando el grafo.

        print("Estados del AFD: ", self.estados_AFD)
        print("Estados finales del AFD: ", self.estados_FinalesE)
        
        # for t in self.trans_AFD:
        #     print(str(t))
        
        # print("Estado inicial AFD: ", self.estado_inicial_AFD)

        estados = self.estados_AFD # Lista de estados del AFD.

        print(type(estados))


        # Convirtiendo la lista de estados en un diccionario.
        diccionario_estados = {}

        for i in self.trans_AFD:
            if i.estadoInicial in diccionario_estados:
                diccionario_estados[i.estadoInicial].append((i.simbolo, i.estadoFinal))
            else: 
                diccionario_estados[i.estadoInicial] = [(i.simbolo, i.estadoFinal)]

        print("Diccionario de estados: ", diccionario_estados)

        # Creando el diccionario de transiciones.
        for key, value in diccionario_estados.items():
            
            print("Estado: ", key, "Transiciones: ", value)

            # Dibujando las transiciones.
            for simbolo, estado in value:
                grafo.edge(key, estado, label=simbolo)

        
        

        # Dibuja los estados del AFD.
        for estado in estados:
            if estado in self.estados_FinalesE:
                grafo.node(estado, estado, shape="doublecircle")
            else:
                grafo.node(estado, estado, shape="circle")

        
        # Colocando el autómta de manera horizontal.
        grafo.graph_attr['rankdir'] = 'LR'

        grafo.render('grafo2', view=True) # Dibujando el grafo.