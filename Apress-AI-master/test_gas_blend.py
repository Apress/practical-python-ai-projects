
from gas_blend import gen_raw, gen_refined, solve_gas
def main():
    import sys
    import random
    import tableutils

    n=8
    m=3
    if len(sys.argv)<=1:
        print('Usage is main [raw|ref|run] [seed]')
        return
    elif len(sys.argv)>=3:
        random.seed(int(sys.argv[2]))
    C=gen_raw(n)
    D=gen_refined(m)
    if sys.argv[1]=='raw':
        for i in range(n):
            C[i].insert(0,'R'+str(i))
        C.insert(0,['Gas','Octane', 'Availability','Cost'])
        tableutils.printmat(C)
    elif sys.argv[1]=='ref':
        for i in range(m):
            D[i].insert(0,'F'+str(i))
        D.insert(0,['Gas','Octane','Min demand.', 'Max demand.','Price'])
        tableutils.printmat(D)
    elif sys.argv[1]=='run':
        rc,Value,G=solve_gas(C,D)
        Price=0.0
        Cost=0.0
        T=[]
        for i in range(n+2):
            T=T+[[0]*(2+m)]
        for i in range(n):
            for j in range(m):
                T[i][j] = round(G[i][j],2)
            T[i][m]=round(sum([G[i][j] for j in range(m)]),2)
            T[i][m+1]=round(sum([G[i][j]*C[i][2] for j in range(m)]),2)
            Price += sum([G[i][j]*D[j][3] for j in range(m)])
        for j in range(m):
            T[n][j]=round(sum(G[i][j] for i in range(n)),2)
            T[n+1][j]=round(sum([G[i][j]*D[j][3] for i in range(n)]),2)
            Cost += sum([G[i][j]*C[i][2] for i in range(n)])
        T.insert(0,['F0','F1','F2','Barrels','Cost'])
        for i in range(len(T)):
            if i == 0:
               T[i].insert(0,"")
            elif i <= n:
               T[i].insert(0,"R"+str(i-1))
            elif i == n+1:
               T[i].insert(0,"Barrels")
            else:
               T[i].insert(0,"Price")
        T[2+n][2+m]='{0:.2f}'.format(Price-Cost)
        tableutils.printmat(T)
main()
