import numpy as np
from scipy.sparse import spdiags

def sparseMatrix(cantidad):
    N = cantidad-1 # cantidad de nodos interiores
    diagonal_unos = -1*np.ones(N)
    diagonal_cuatros = 4*np.ones(N)

    datos = np.array([diagonal_unos, diagonal_cuatros, diagonal_unos])
    diagonales = np.array([-1,0,1])
    return spdiags(datos, diagonales, N+1, N+1).toarray()


def dfMatrix(cantidad):
    N = cantidad - 1
    retorno = np.array([])
    I = -1*np.identity(N)
    B = sparseMatrix(N)
    
    for i in range(N):
        for j in range(N):
            if j == i:
                if j == 0:
                    auxiliar = B
                else:
                    auxiliar = np.concatenate((auxiliar, B), axis=1)
            else:
                if j == 0:
                    if j == i - 1:
                        auxiliar = I
                    else:
                        auxiliar = np.zeros((N,N))
                else:
                    if j == i - 1 or j == i+1:
                        auxiliar = np.concatenate((auxiliar, I), axis=1)
                    else:
                        auxiliar = np.concatenate((auxiliar, np.zeros((N,N))), axis=1)
        if i == 0:
            retorno = auxiliar
        else:
            retorno = np.concatenate((retorno, auxiliar), axis=0)
    return retorno

def solutionVector(funcion_objetivo, cantidad, a=0,b=1):
    N = cantidad-1
    h = (b-a)/cantidad
    retorno = np.array([])
    
    for i in range(1,N+1):
        for j in range(1,N+1):
            valor = funcion_objetivo(i*h,j*h)
            auxiliar = np.ones((1,1)) * valor
            if i == 1 and j == 1:
                retorno = auxiliar
            else:
                retorno = np.concatenate((retorno, auxiliar), axis=0)
    return retorno