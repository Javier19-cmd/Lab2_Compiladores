from reg import evaluar
from Thompson import thompson, graficar, grafo
from Errores import *

inp = input("Ingrese la expresion regular: ")

verificacion = deteccion(inp) # Verificando que la expresión regular sea correcta.

if verificacion == True: # Si la expresión regular es correcta, se procede a evaluarla.
    
    regex = evaluar(inp)
    print("La expresion regular es correcta.")
    print("La expresion regular es: ", regex)
    automata, lista, diccionario = thompson(regex)
    #graficar(automata, lista, diccionario)
    grafo(automata, lista, diccionario)

else:
    print("La expresion regular es incorrecta.")

# Arreglar el problema de paréntesis sin abrir.
