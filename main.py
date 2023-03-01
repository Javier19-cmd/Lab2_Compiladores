from reg import evaluar
from Thompson import thompson, graficar, grafo, alfabeto
from Errores import *
from AFD_Converter import *
import re 

inp = input("Ingrese la expresion regular: ")


# Recorriendo la expresión regular para verificar si hay un ? para cambiarlo por un a|ε.
if "?" in inp:
    inp = inp.replace("?", "|ε")


verificacion = deteccion(inp) # Verificando que la expresión regular sea correcta.

if verificacion == True: # Si la expresión regular es correcta, se procede a evaluarla.
    
    regex = evaluar(inp)
    alfabeth = alfabeto(regex)
    print("La expresion regular es correcta.")
    print("La expresion regular es: ", regex)
    automata, lista, diccionario = thompson(regex)
    
    
    #graficar(automata, lista, diccionario)
    grafo(automata, lista, diccionario)

    # Haciendo la conversión a AFD.
    AFD(alfabeth, automata, lista, diccionario)

else:
    print("La expresion regular es incorrecta.")
