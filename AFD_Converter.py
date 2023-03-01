"""
Archivo que se encargará de convertir el autómata finito no determinista a un autómata finito determinista.
"""

class AFD:

    def __init__(self, alfabeto, automata, transiciones, diccionario):
        self.alfabeto = alfabeto
        self.automata = automata
        self.transiciones = transiciones
        self.diccionario = diccionario

        self.conversion()

    def conversion(self): # Método para convertir el AFD a AFD.
        # Imprimiendo los datos del autómata.

        print(self.automata)
        print(self.diccionario)

        estado_inicial = self.eclosure(self.automata.estado_inicial) # Calculand el estado inicial del autómata.

        #print(estado_inicial) # Imprimiendo el estado inicial.

        estdos_AFD = [estado_inicial] # Creando la lista de estados_AFD y guardando su primer estado.
        
        t_trans = {} # Creando la tabla de transición de los estados.

        estados_a_revisar = [estado_inicial] # Creando la lista de estados a revisar.

        # print(estados_a_revisar, "Estados a revisar")
        # print(estdos_AFD, "Estados AFD")

        while len(estados_a_revisar) > 0: # Mientras la lista de estados a revisar no esté vacía.
            estado_actual = estados_a_revisar.pop() # Sacando el último elemento de la lista de estados a revisar.

            #print("Estado actual: ", estado_actual)

            for simbolo in self.alfabeto: # Recorriendo el alfabeto.
                # Por cada símbolo, se calcula el conjunto de estados alcanzables desde el estado actual.
                estado_alcanzable = self.eclosure(self.move(estado_actual, simbolo))

                if estado_alcanzable: # Si el conjunto de estados alcanzables no está vacío.
                    if estado_alcanzable not in estdos_AFD: # Si el conjunto de estados alcanzables no está en la lista de estados_AFD.
                        estdos_AFD.append(estado_alcanzable) # Se agrega el conjunto de estados alcanzables a la lista de estados_AFD.
                        estados_a_revisar.append(estado_alcanzable) # Se agrega el conjunto de estados alcanzables a la lista de estados a revisar.
                    
                    t_trans[(tuple(estado_actual), simbolo)] = tuple(estado_alcanzable) # Creando la tupla para la tabla de transición.

        # Almacenando los estados finales del AFD.
        estados_finales = []

        # for estado in estdos_AFD: # Recorriendo la lista de estados_AFD.
        #     for estado_final in self.automata.estado_final: # Recorriendo la lista de estados finales del AFD.
        #         if estado_final in estado: # Si el estado final está en el conjunto de estados.
        #             estados_finales.append(estado) # Se agrega el conjunto de estados a la lista de estados finales.

        #print("Estados AFD: ", estdos_AFD)
        print("Transiciones: ", t_trans)

        # # Detectando los estados finales en el diccionario de transiciones.
        # for key, value in t_trans.items(): 
        #     print(key, value)

        #     if self.automata.estado_final in key or self.automata.estado_final in value:
        #         print("Estado final detectado")

        # # for transicion in self.transiciones: 
        # #     print(str(transicion))

        # # Creando un diccionario para guardar los conjuntos que se generan, a cual conjunto llega con cada símbolo del alfabeto.
        # conjuntos = {}

        # # Diccionario para guardar los movimientos con cada símbolo del alfabeto.
        # movimientos = {}
        
        # # Primer paso: Calcular cerradura epsilon del estado inicial.
        # # Para esto, se necesita el estado inicial y el diccionario de transiciones.
        # ecr = self.eclosure(self.automata.estado_inicial) # Resultado de la cerradura epsilon del estado inicial.

        # # Segundo paso: Calcular los movimientos con cada símbolo del alfabeto.
        # # Para esto, se necesita el alfabeto, el estado que se regresa de la cerradura epsilon y el diccionario de transiciones.
        # for simbolo in self.alfabeto: # Recorriendo el alfabeto.
        #     #print("Símbolo: ", simbolo)
        #     moves = self.move(ecr, simbolo) # Calculando el conjunto de estados alcanzables desde el conjunto de estados que se regresa de la cerradura epsilon.
        #     #a = self.eclosure(moves)
        #     #print("Conjunto: ", a)

        #     # Guardando los movimientos en el diccionario.
        #     movimientos[simbolo] = moves

        # print("Movimientos: ", movimientos)

        # # Tercer paso: Calcular el cierre epsilon de cada conjunto de estados que se obtiene en el paso anterior.
        # for key, value in movimientos.items(): # Recorriendo el diccionario de movimientos.
        #     print("Key: ", key)
        #     # Calculando el cierre epsilon de cada estado del conjunto de estados.
        #     for estado in value:
        #         #print("Estado: ", estado)
        #         ecr1 = self.eclosure(estado)
        #         #print("Cierre epsilon: ", ecr)

        #         # Guardando el conjunto de estados en el diccionario de la forma {conjunto: {simbolo, conjunto}}.
        #         conjuntos[ecr1] = {key: ecr}
        
        # print("Conjuntos: ", conjuntos)
        # #print("Alfabeto: ", self.alfabeto)


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
    
    def move(self, conjunto, simbolo): # Método para calcular el conjunto de estados alcanzables desde un conjunto de estados.

        # print("Conjunto: ", conjunto)
        # print("Símbolo: ", simbolo)
        
        result = 0 # Lista para el resultado.

        #pila = [] # Stack para realizar el procedimiento.

        # Verificando que movimientos se pueden hacer con el símbolo.
        for estado in conjunto: # Recorriendo el conjunto de estados.
            #print("Estado: ", estado)

            for esta in self.diccionario[estado]:
                #print("Transición: ", esta)

                if esta[0] == simbolo:
                    #print("Llegué al if")
                    #print(esta[1])
                    result = esta[1]

        #print("Resultado: ", result)
        return result 
