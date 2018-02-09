
from blend_multi import gen_data_content, gen_data_target, gen_data_cost, gen_data_inventory, solve_model
def main():
    import sys
    import random
    import tableutils
    m=9 
    n=7
    k=5
    if len(sys.argv)<=1:
        print('Usage is main [content|target|cost|inventory|run] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    C=gen_data_content(m,n)
    T=gen_data_target(C)
    K=gen_data_cost(m,k)
    I=gen_data_inventory(m)
    if sys.argv[1]=='content':
        for j in range(m):
            C[j].insert(0,'O'+str(j))
        C.insert(0,['']+['A'+str(i) for i in range(n)])
        tableutils.printmat(C,False,1)
    elif sys.argv[1]=='target':
        T.insert(0,['']+['A'+str(i) for i in range(n)])
        T[1].insert(0,'Min')
        T[2].insert(0,'Max') 
        tableutils.printmat(T,True,1)
    elif sys.argv[1]=='cost':
        for j in range(m):
            K[j].insert(0,'O'+str(j))
        K.insert(0,['']+['Month '+str(i) for i in range(k)])
        tableutils.printmat(K)
    elif sys.argv[1]=='inventory':
        for j in range(m):
            I[j].insert(0,'O'+str(j))
        I.insert(0,['Oil','Held'])
        tableutils.printmat(I)
    elif sys.argv[1]=='run':
        Demand=5000
        Limits=[500,2000]
        Cost=5
        rc,Value,B,L,H,P,A,CP,CS=solve_model(C,T,K,I,Demand,Cost,Limits)
        if len(B):
            A.append([0 for l in range(len(A[0]))])
            for j in range(len(A)-1):
                for l in range(len(A[0])):
                    A[j][l] = A[j][l]/P[l]
                    A[-1][l] += A[j][l] 
            for j in range(m):
                B[j].insert(0,'O'+str(j))
                L[j].insert(0,'O'+str(j))
                H[j].insert(0,'O'+str(j))
            for l in range(n):
                A[l].insert(0,'A'+str(l))
            A[-1].insert(0,'Total')
            B.insert(0,['Buy qty']+['Month '+str(i) for i in range(k)])
            L.insert(0,['Blend qty']+['Month '+str(i) for i in range(k)])
            H.insert(0,['Hold qty']+['Month '+str(i) for i in range(k)])
            A.insert(0,['Acid %']+['Month '+str(i) for i in range(k)])
            P=[P]
            P[0].insert(0,'Prod qty')
            CP=[CP]
            CP[0].insert(0,'P. Cost')
            CS=[CS]
            CS[0].insert(0,'S. Cost')

            tableutils.printmat(B,True,1)
            tableutils.printmat(L,True,1)
            tableutils.printmat(H,True,1)
            tableutils.printmat(P,True,1)
            tableutils.printmat(CP,True,2)
            tableutils.printmat(CS,True,2)
            tableutils.printmat(A,True,1)

main()
