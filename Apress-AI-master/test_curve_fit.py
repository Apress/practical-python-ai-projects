
from curve_fit import gen_data, solve_model
def main():
    import sys
    import random
    import tableutils
    n=10
    degree=2
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>=2:
        random.seed(int(sys.argv[2]))
    C=gen_data(lambda t:  1.8*t*t - 1.5*t + 0.3, n)
    if sys.argv[1]=='data':
        C.insert(0,['$t_i$','$f_i$'])
        tableutils.printmat(C,True)
    elif sys.argv[1]=='run':
        rc0,v,G=solve_model(C,degree,0)
        rc1,v,G1=solve_model(C,degree,1)
        T=[]
        error=0
        for i in range(n):
            fti = sum(G[j]*C[i][0]**j for j in range(degree+1))
            fti1 = sum(G1[j]*C[i][0]**j for j in range(degree+1))
            error += abs(fti - C[i][1])
            T.append([C[i][0], C[i][1], fti, abs(C[i][1]-fti), fti1, abs(C[i][1]-fti1)])
        T.insert(0,['$t_i$','$f_i$', '$f_{sum}(t_i)$', '$e_i^{sum}$', '$f_{max}(t_i)$', '$e_i^{max}$'])          
        tableutils.printmat(T,True)

main()
