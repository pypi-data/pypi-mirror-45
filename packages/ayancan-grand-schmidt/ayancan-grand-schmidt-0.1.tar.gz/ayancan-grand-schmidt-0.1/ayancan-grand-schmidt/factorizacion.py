import numpy as np
from numpy.linalg import norm, qr

np.seterr(divide='ignore', invalid='ignore')

def initializeMatrix(A):
    m = len(A)
    n = len(A[0])
    v = np.zeros((m, n))
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    return m,n,v,Q,R

def gramSchimdtClassic(A):
    _, n,v,Q,R = initializeMatrix(A)

    for j in range(0,n): # from 1 to n
        v[:,[j]] = A[:,[j]] # vj = aj
        for i in range(0,j): # for i=1 to j-1
            aux1 = np.append([], Q[:,[i]])
            aux1 = np.transpose(np.conj(aux1))
            aux2 = np.append([], A[:,[j]])
            resultado = np.dot(aux1, aux2)
            R[i][j] = resultado
            v[:,[j]] = v[:,[j]] - R[i][j]*Q[:,[i]]
        R[j][j] = norm(v[:,[j]])
        Q[:,[j]] = v[:,[j]]/R[j][j]
    return Q, R

def gramSchimdtModern(A):
    _, n,v,Q,R = initializeMatrix(A)
    for i in range(n):
        v[:,[i]] = A[:,[i]]

    for i in range(n):
        R[i][i] = norm(v[:,[i]])
        Q[:, [i]] = v[:, [i]]/R[i][i]
        for j in range(i+1,n):
            aux1 = np.append([], Q[:, [i]])
            aux1 = np.transpose(np.conj(aux1))
            aux2 = np.append([], v[:, [j]])
            R[i][j] = np.dot(aux1, aux2)
            v[:, [j]] = v[:, [j]] - R[i][j]*Q[:, [i]]
    return Q, R


if __name__ == "__main__":
    # example code
    exampleMatrix = np.array([[1,2,3],[-3,0,1],[1,0,0],[-8,9-5]])
    qClassic, rClassis = gramSchimdtClassic(exampleMatrix)
    qModern, rModern = gramSchimdtModern(exampleMatrix)