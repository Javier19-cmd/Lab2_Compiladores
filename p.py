def hopcroft_minimization(Q, Sigma, delta, q0, F):
    # División inicial del autómata en dos conjuntos
    P = [F, list(set(Q) - set(F))]
    W = [F]
    while W:
        A = W.pop(0)
        for a in Sigma:
            X = []
            for q in A:
                X.append(delta[q][a])

                print("Delta: ", delta[q][a])

            for Y in P:
                Y_int_X = list(set(Y).intersection(set(X)))
                Y_minus_X = list(set(Y) - set(X))
                X_minus_Y = list(set(X) - set(Y))
                if Y_int_X and Y_minus_X:
                    P.remove(Y)
                    P.extend([Y_int_X, Y_minus_X])
                    if Y in W:
                        W.remove(Y)
                        W.extend([Y_int_X, Y_minus_X])
                    else:
                        if len(Y_int_X) <= len(Y_minus_X):
                            W.append(Y_int_X)
                        else:
                            W.append(Y_minus_X)
    
    # Creación del autómata mínimo
    Q_min = []
    delta_min = {}
    q0_min = None
    F_min = []
    for X in P:
        Q_min.append(X[0])
        delta_min[X[0]] = {}
        for a in Sigma:
            for Y in P:
                if X[0] in Y:
                    delta_min[X[0]][a] = Y[0]
                    break
    for X in P:
        if q0 in X:
            q0_min = X[0]
            break
    for X in P:
        if set(X).intersection(set(F)):
            F_min.append(X[0])
    return Q_min, Sigma, delta_min, q0_min, F_min


Q = ['A', 'B', 'C', 'D', 'E']
Sigma = ['0', '1']
delta = {'A': {'0': 'B', '1': 'C'}, 'B': {'0': 'B', '1': 'D'},
         'C': {'0': 'B', '1': 'C'}, 'D': {'0': 'E', '1': 'C'},
         'E': {'0': 'B', '1': 'C'}}
q0 = 'A'
F = ['B', 'D', 'E']
Q_min, Sigma_min, delta_min, q0_min, F_min = hopcroft_minimization(Q, Sigma, delta, q0, F)
print(Q_min)
print(Sigma_min)
print(delta_min)
print(q0_min)
print(F_min)
