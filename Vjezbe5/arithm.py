import numpy as np

def algoritam(L):
    suma = 0
    S = sum(L)/len(L)
    for i in L:
        A =(i-S)**2
        suma+=A
    sigma=np.sqrt(suma/(len(L)*(len(L)-1)))
    print(S,sigma)
algoritam([1,2,3,4,5,6,7,8,9,10])