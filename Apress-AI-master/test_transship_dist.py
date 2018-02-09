
import transship_dist
def main():
    import sys
    import random
    import tableutils
    n=8
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>=2:
        random.seed(int(sys.argv[2]))
    C=transship_dist.gen_data(n)
    if sys.argv[1]=='data':
        for i in range(n):
            C[i].insert(0,'N'+str(i))
        C[-1].insert(0,'Demand')
        C.insert(0,['From/To']+['N'+str(i) for i in range(n)]+['Supply'])
        tableutils.printmat(C)
    elif sys.argv[1]=='run':
        rc,V,G=transship_dist.solve_model(C)
        if rc != 0:
            print('Infeasible')
        else:
            T=[]
            for i in range(n):
                T.append([0 for j in range(n+1)])
                tot = 0
                for j in range(n):
                    T[i][j] = int(G[i][j])
                    tot += int(G[i][j])
                T[i][-1] = tot
            TT = []
            for j in range(n):
                TT.append(sum([T[i][j] for i in range(n)]))
            TT.insert(0,'In')
            T.append(TT)
            for i in range(n):
                T[i].insert(0,'N'+str(i))

            T.insert(0,['From/To']+['N'+str(i) for i in range(n)]+['Out'])
            
            tableutils.printmat(T)
main()
