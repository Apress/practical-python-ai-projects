
from job_shop import gen_data, solve_model
def main():
    import sys
    import random
    import tableutils
    m=4
    n=3
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    D=gen_data(m,n)
    if sys.argv[1]=='data':
        T=[]
        for i in range(m):
            T.append([str(D[i][j][0])+'-'+str(D[i][j][1]) for j in range(n)])
        left=['J'+str(i) for i in range(m)]
        header=['Job']+['Machine-Duration' for _ in range(n)]
        T=tableutils.wrapmat(T,left,header)
        tableutils.printmat(T,True)
    elif sys.argv[1]=='run':
        rc,Val,x=solve_model(D)
        T=[[tableutils.set2string((x[i][D[i][k][0]], D[i][k][0], D[i][k][1])) for k in range(n) if D[i][k][1]>0] for i in range(m)]
        T=tableutils.wrapmat(T,['Job:'+str(i) for i in range(m)],['(S; M; D)' for _ in range(n)])
        tableutils.printmat(T,True)


main()
