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

        for transicion in self.transiciones: 
            print(str(transicion))
        
        # Primer paso: Calcular cerradura epsilon del estado inicial.
        # Para esto, se necesita el estado inicial y el diccionario de transiciones.
        # print("Estado inicial: ", self.automata.estado_inicial)
        self.eclosure(self.automata.estado_inicial)
        
        print("Alfabeto: ", self.alfabeto)

    def eclosure(self, estado): #Método para calcular el cierre epsilon de un estado.
        print("Estado: ", estado)