
from mincost import gen_data, solve_model
def main():
    import sys
    import random
    import tableutils
    m=3
    n=7
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>=2:
        random.seed(int(sys.argv[2]))
    C=gen_data(m,n)
    if sys.argv[1]=='data':
        for i in range(m):
            C[i].insert(0,'Plant '+str(i))
        C[-1].insert(0,'Demand')
        C.insert(0,['From/To']+['City '+str(i) for i in range(n)]+['Supply'])
        tableutils.printmat(C)
    elif sys.argv[1]=='run':
        rc,Value,G=solve_model(C)
        T=[]
        for i in range(m):
            T.append([0 for j in range(n+1)])
            tot = 0
            for j in range(n):
                T[i][j] = int(G[i][j])
                tot += int(G[i][j])
            T[i][-1] = tot
        TT = []
        for j in range(n):
            TT.append(sum([T[i][j] for i in range(m)]))
        TT.insert(0,'Total')
        T.append(TT)
        for i in range(m):
            T[i].insert(0,'Plant '+str(i))

        T.insert(0,['From/To']+['City '+str(i) for i in range(n)]+['Total'])
            
        tableutils.printmat(T)


main()
