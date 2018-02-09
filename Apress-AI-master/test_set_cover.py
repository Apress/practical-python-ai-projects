
from set_cover import gen_data, solve_model
def main():
    import sys
    import random
    import tableutils
    m=15
    n=25
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    D,C=gen_data(m,n)
    if sys.argv[1]=='data':
        T=[]
        for i in range(m):
            T.append([tableutils.set2string(D[i])])
        T=tableutils.splitwrapmat(T,['S'+str(i) for i in range(m)],['Supplier','Part numbers'])
        tableutils.printmat(T,True)
    elif sys.argv[1]=='run':
        rc,Val,S,P=solve_model(D,None)
        T=[]
        for i in range(len(P)):
            T.append([tableutils.set2string(P[i])])
        T.insert(0,[tableutils.set2string(S)])
        T=tableutils.splitwrapmat(T,['All']+['Part #'+str(j) for j in range(n)],['Parts','Suppliers'])
        tableutils.printmat(T,True)


main()
