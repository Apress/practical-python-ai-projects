
from project_management import gen_data, solve_model, solve_model_clp
def main():
    import sys
    import random
    import tableutils
    n=12
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>=3:
        random.seed(int(sys.argv[2]))
    C=gen_data(n)
    if sys.argv[1]=='data':
        T=[]
        for i in range(n):
            TT=[C[i][0],C[i][1]]
            s='{'
            for j in C[i][2]:
                s = s+' '+str(j)
            s=s+' }'
            TT.append(s)
            T.append(TT)
        T.insert(0,['Task', 'Duration','Preceding tasks'])
        tableutils.printmat(T,True)
    elif sys.argv[1]=='run' or sys.argv[1]=='runclp':
        if sys.argv[1]=='run':
            rc,V,G=solve_model(C)
        else:
            rc,V,G=solve_model_clp(C)
        T=[]
        TT=['Task']+[C[i][0] for i in range(n)]
        T.append(TT)
        TT=['Start']+[int(G[i]) for i in range(n)]
        T.append(TT)
        TT=['End']+[int(G[i]+C[i][1]) for i in range(n)]
        T.append(TT)
        tableutils.printmat(T,True)

main()
