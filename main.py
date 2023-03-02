from reg import evaluar
from Thompson import thompson, graficar, grafo, alfabeto
from Errores import *
from AFD_Converter import *
from AFD_Directo import *
import re

inp = input("Ingrese la expresion regular: ")


# Recorriendo la expresión regular para verificar si hay un ? para cambiarlo por un a|ε.
if "?" in inp:
    inp = inp.replace("?", "|ε")

# Recorriendo la expresión regular para hacer la idempotencia de la cerradura de Kleene (o sea si hubiera un a**** cambiarlo a a*)
if "*" in inp:
    inp = inp.replace("*****************", "*")
    inp = inp.replace("****************", "*")
    inp = inp.replace("***************", "*")
    inp = inp.replace("**************", "*")
    inp = inp.replace("************", "*")
    inp = inp.replace("**********", "*")
    inp = inp.replace("********", "*")
    inp = inp.replace("******", "*")
    inp = inp.replace("*****", "*")
    inp = inp.replace("****", "*")
    inp = inp.replace("***", "*")
    inp = inp.replace("**", "*")

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

    # Haciendo la conversión a AFD directo.
    AFD_Directo(regex)

else:
    print("La expresion regular es incorrecta.")
