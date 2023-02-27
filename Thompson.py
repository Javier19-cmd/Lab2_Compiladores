from Estado import *
from Automata import *
from Transiciones import *
import matplotlib.pyplot as plt
import networkx as nx
import graphviz as gv

def thompson(expresion_regular):
    """Convierte una expresión regular en un autómata utilizando el algoritmo de Thompson"""
    stack = []
    lista = []
    diccionario = {}
    estados = 0
    epsilon = 'ε'

    for caracter in expresion_regular:
        if caracter == '|':
            # Obtener los dos últimos automatas del stack
            b = stack.pop()
            a = stack.pop()


            # Crear nuevos estados inicial y final
            inicio = Estado(estados)
            estados += 1
            fin = Estado(estados)
            estados += 1

            # Crear transiciones epsilon desde los nuevos estados inicial y final a los automatas a y b.

            # Creando las transiciones epsilon desde el estado inicial al estado inicial de a y b.
            nuevo1 = Transiciones(inicio, 'ε', a.get_estado_inicial())
            nuevo2 = Transiciones(inicio, 'ε', b.get_estado_inicial())
            nuevo3 = Transiciones(a.get_estado_final(), 'ε', fin)
            nuevo4 = Transiciones(b.get_estado_final(), 'ε', fin)

            # Crear el nuevo autómata y apilarlo en el stack  
            nuevo_automata = Automata(inicio, fin)
            
            # Agregando los nuevos estados a la lista de estados.
            lista.append(nuevo1)
            lista.append(nuevo2)
            lista.append(nuevo3)
            lista.append(nuevo4)

            # Guardando el nuevo automata en el stack.
            stack.append(nuevo_automata)

        elif caracter == '*':
            # Obtener el último automata del stack
            a = stack.pop()

            # Crear nuevos estados inicial y final
            inicio = Estado(estados)
            estados += 1
            fin = Estado(estados)
            estados += 1

            # Crear transiciones epsilon desde los nuevos estados inicial y final a los estados inicial y final del automata a
            n1 = Transiciones(inicio, 'ε', a.get_estado_inicial())
            n2 = Transiciones(inicio, 'ε', fin)
            n3 = Transiciones(a.get_estado_final(), 'ε', a.get_estado_inicial())
            n4 = Transiciones(a.get_estado_final(), 'ε', fin)

            # Crear el nuevo autómata y apilarlo en el stack
            nuevo_automata = Automata(inicio, fin)
            stack.append(nuevo_automata)

            # Agregando los nuevos estados a la lista de estados.
            lista.append(n1)
            lista.append(n2)
            lista.append(n3)
            lista.append(n4)

        elif caracter == '+':
            # Obtener el último automata del stack
            a = stack.pop()

            # Crear nuevos estados inicial y final
            inicio = Estado(estados)
            estados += 1
            fin = Estado(estados)
            estados += 1

            # Crear transiciones epsilon desde los nuevos estados inicial y final a los estados inicial y final del automata a
            
            nu1 = Transiciones(inicio, 'ε', a.get_estado_inicial())
            nu2 = Transiciones(a.get_estado_final(), 'ε', a.get_estado_inicial())
            nu3 = Transiciones(a.get_estado_final(), 'ε', fin)

            # Crear el nuevo autómata y apilarlo en el stack
            nuevo_automata = Automata(inicio, fin)
            stack.append(nuevo_automata)
            
            # Agregando los nuevos estados a la lista de estados.
            lista.append(nu1)
            lista.append(nu2)
            lista.append(nu3)

        elif caracter == '.':
            # Obtener los dos últimos automatas del stack
            b = stack.pop()
            a = stack.pop()

            # # Obteniendo el estado final del autómata b. (segundo autómata)
            # print(b.get_estado_final())

            # # Obteniendo el estado inicial del autómata a. (primer autómata)
            # print(a.get_estado_inicial())

            # Sacando la información de los estados.
            estadoFinal = a.get_estado_final()
            estadoInicial = b.get_estado_inicial()

            # print("Estado final: ", estadoFinal)
            # print("Estado inicial: ", estadoInicial)

            # Merge de los estados.
            for transicion in lista: 

                if transicion.getEstadoInicial() == estadoInicial:
                    
                    transicion.setEstadoInicial(estadoFinal)

                # if i.getEstadoInicial() == b.get_estado_inicial():
                #     # Creando una transición desde el estado inicial del autómata a al estado final del autómata b.
                #     n = Transiciones(a.get_estado_final(), i.getSimbolo(), b.get_estado_final())
                #     # Eliminando la transición del estado inicial del autómata b.
                #     lista.remove(i) 
                #     # Agregando la nueva transición a la lista de transiciones.
                #     lista.append(n)

                #     print("Transición: ", n)

            # Crear el nuevo autómata y apilarlo en el stack
            nuevo_automata = Automata(a.get_estado_inicial(), b.get_estado_final())
            stack.append(nuevo_automata)

            # # Crear el nuevo autómata y apilarlo en el stack
            # nuevo_automata = Automata(a.estado_inicial, b.estado_final)
            
            # stack.append(nuevo_automata)
            # lista.append(nuevo_automata)
        
        elif caracter == '?': # Operador de cero o una ocurrencia.
            # Este operador es equivalente a la expresión regular (a|ε).
            
            # Haciendo primero una transición con dos estados y ε.
            inicio1 = Estado(estados)
            estados += 1
            fin1 = Estado(estados)
            estados += 1

            # Creando la transición.
            en1 = Transiciones(inicio1, epsilon, fin1)
            lista.append(en1)
            nuevo_automata1 = Automata(inicio1, fin1)
            stack.append(nuevo_automata1)

            # Obtener los dos últimos automatas del stack
            b = stack.pop()
            a = stack.pop()


            # Crear nuevos estados inicial y final
            inicio2 = Estado(estados)
            estados += 1
            fin2 = Estado(estados)
            estados += 1

            # Crear transiciones epsilon desde los nuevos estados inicial y final a los automatas a y b.

            # Creando las transiciones epsilon desde el estado inicial al estado inicial de a y b.
            ns1 = Transiciones(inicio2, 'ε', a.get_estado_inicial())
            ns2 = Transiciones(inicio2, 'ε', b.get_estado_inicial())
            ns3 = Transiciones(a.get_estado_final(), 'ε', fin2)
            ns4 = Transiciones(b.get_estado_final(), 'ε', fin2)

            # Crear el nuevo autómata y apilarlo en el stack  
            nuevo_automata2 = Automata(inicio2, fin2)
        
            # Guardando el nuevo automata en el stack.
            stack.append(nuevo_automata2)

            # Agregando los nuevos estados a la lista de estados.
            lista.append(ns1)
            lista.append(ns2)
            lista.append(ns3)
            lista.append(ns4)

            print("Lista: ", str(lista))

        else:
            # Crear nuevos estados inicial y final para el autómata que representa el caracter actual.
            # Crear nuevos estados inicial y final
            inicio = Estado(estados)
            estados += 1
            fin = Estado(estados)
            estados += 1

            # # Crear transición desde el estado inicial al estado final con el caracter actual.
            trans = Transiciones(inicio, caracter, fin)
            
            # # Crear el nuevo autómata y apilarlo en el stack
            nuevo_automata = Automata(inicio, fin)
            
            # print(nuevo_automata.get_estado_inicial())
            # print(nuevo_automata.get_estado_final())
            
            # Guardando las transiciones de la forma (estado_inicial, caracter, estado_final) en un diccionario.
            stack.append(nuevo_automata)

            # Agregando los nuevos estados a la lista de estados.
            lista.append(trans)

    # for automata in lista:
    #     print(str(automata))

    # # Imprimedo el inicio y el final del autómata.
    # print("Estado inicial: " + str(stack[0].get_estado_inicial()))
    # print("Estado final: " + str(stack[0].get_estado_final()))

    # Convirtiendo la lista de transiciones en un diccionario.
    for i in lista:
        if i.getEstadoInicial() in diccionario:
            diccionario[i.getEstadoInicial()].append((i.getSimbolo(), i.getEstadoFinal()))
        else:
            diccionario[i.getEstadoInicial()] = [(i.getSimbolo(), i.getEstadoFinal())]

        # Guardando el estado final del autómata.
        if i.getEstadoFinal() not in diccionario:
            diccionario[i.getEstadoFinal()] = []

    # for key, value in diccionario.items():
    #     print(key, str(value))

    auto = stack.pop() # Regresando los estados iniciales y finales.

    return auto, lista, diccionario

def req(simbolo):
    # Método para hacer la transición de un estado a otro con epsilon.
        # Crear nuevos estados inicial y final para el autómata que representa el caracter actual.
        # Crear nuevos estados inicial y final
        inicio = Estado(estados)
        estados += 1
        fin = Estado(estados)
        estados += 1

        # # Crear transición desde el estado inicial al estado final con el caracter actual.
        trans = Transiciones(inicio, simbolo, fin)
        
        # # Crear el nuevo autómata y apilarlo en el stack
        nuevo_automata = Automata(inicio, fin)
        
        return trans, nuevo_automata

def graficar(automata, lista, diccionario): #Método para graficar el autómata.

    # Cambiando el título de la ventana.
    plt.title("Autómata Finito No Determinista - Thompson")

    #print(automata)
    
    # # Imprimiendo la lista.
    # for automata in lista:
    #     print(str(automata))

    # # Imprimiedo el diccionario.
    # for key, value in diccionario.items():
    #     print(key, str(value))

    # Colocando en un texto el estado inicial y el estado final.
    #plt.text(0.5, 0.5, "Estado inicial: " + str(automata.get_estado_inicial()) + " Estado final: " + str(automata.get_estado_final()), fontsize=10)


    G = nx.DiGraph() # Creando el grafo.

    print("Diciconario: " + str(diccionario))

    # Agregando los estados al grafo.
    for estado in diccionario:
        G.add_node(estado)

        # Verificando si el estado es inicial o final.
        if estado == automata.get_estado_inicial():
            G.nodes[estado]['color'] = 'green'
        elif estado == automata.get_estado_final():
            G.nodes[estado]['color'] = 'red'
        else:
            G.nodes[estado]['color'] = 'blue'

    # Añadiendo las aristas al grafo.
    for key, value in diccionario.items():
        for simbolo, estado in value:
            for i in lista:
                G.add_edge(key, estado, label=simbolo)

    
    # Configurar opciones de visualización
    pos = nx.spring_layout(G)
    node_colors = [G.nodes[estado]["color"] for estado in G.nodes()]
    edge_labels = {(origen, destino): datos["label"] for origen, destino, datos in G.edges(data=True)}

    # Dibujar el grafo
    nx.draw_networkx_nodes(G, pos, node_color=node_colors)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis("off")
    plt.show()

def grafo(automata, lista, diccionario):
    grafo = gv.Digraph('G', filename='grafo', format='png')

    estados = [ str(estado) for estado in diccionario.keys() ]

    # Dibujando los nodos.
    for estado in estados:
        if estado == str(automata.get_estado_inicial()):
            grafo.node(estado, estado, color='green')
        elif estado == str(automata.get_estado_final()):
            grafo.node(estado, estado, color='red')
        else:
            grafo.node(estado, estado, color='blue')
    
    # Dibujando las aristas.
    print("Estados: " + str(estados))

    # Dibujando las transiciones.
    for key, value in diccionario.items():
        for simbolo, estado in value:
            grafo.edge(str(key), str(estado), label=simbolo)

    # Colocando el autómta de manera horizontal.
    grafo.graph_attr['rankdir'] = 'LR'

    grafo.render('grafo', view=True)


