
from puzzle import solve_maxrook
from time import time
def main():
    n0,S,X = 8,7,3
    N,T = [],[]
    for i in range(S):
        n = n0*2**i
        N.append(n)
        t0 = time()
        for _ in range(X):
            rc = solve_maxrook(n)
        t = (time()-t0)/X
        T.append(t)
    T  = [T[i]/T[0] for i in range(len(T))]
    for i in range(S):
        print('{0:4d} {1:.0f}'.format(N[i],T[i]))
main()
