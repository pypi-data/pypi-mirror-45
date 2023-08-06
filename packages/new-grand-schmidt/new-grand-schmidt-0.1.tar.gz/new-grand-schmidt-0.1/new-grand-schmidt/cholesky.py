import numpy as np

def cholesky(matriz):
    R = np.array(matriz)
    m = len(matriz[0])
    for k in range(m):                                          # for k = 1 to m
        for j in range(k+1, m):                                 #   for j = k+1 to m
            auxiliar = np.conjugate(R[j][k])/R[k][k]
            R[j:, [j]] = R[j:, [j]] - np.dot(R[j:,[k]],auxiliar)
            R[:j, [j]] = np.zeros(np.shape(R[:j, [j]]))
        R[k:,[k]] = R[k:,[k]] / np.sqrt(R[k][k])
    return R