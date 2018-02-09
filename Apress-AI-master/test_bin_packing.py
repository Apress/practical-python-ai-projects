
from __future__ import print_function
import time, tableutils
from bin_packing import gen_data, solve_model
def main():
    import sys
    import random
    import tableutils
    n=3
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    D,S=gen_data(n)
    if sys.argv[1]=='data':
        T=tableutils.wrapmat(D,[str(i) for i in range(n)],['','nb of packages','Unit weight'])
        T.insert(0,['','Truck weight limit',S])
        T.append(['Total',sum(e[0] for e in D), sum(e[0]*e[1] for e in D)])
        tableutils.printmat(T,True)
    elif sys.argv[1] in ['run', 'run0', 'nrun', 'nrun0']:
        start = time.clock()
        if sys.argv[1] in ['nrun', 'nrun0']:
          rc,Val,P2T,T2P=solve_model(D,S,False)
        else:
          rc,Val,P2T,T2P=solve_model(D,S,True)
        end = time.clock()
        #print 'Elapsed time ', end-start, ' optimal value ', Val
        if rc != 0:
            print('Infeasible')
        else:
            if sys.argv[1] in ['run', 'nrun']:
                w = sum(e[2] for row in T2P for e in row[1] )
                t = sum(1 for row in T2P for e in row[1] if len(row)>0)
                print('Trucks {0}, Packages {2} ({1})'.format(Val,w,t))
                print('(id weight), (id weight)*')
                for row in T2P:
                    if (len(row[1])):              
                        print('{0:2} ({2}),"{1}"'.format(row[0],row[1],sum(e[2] for e in row[1])))
            else: 
                print('Weight, Truck id')
                for row in P2T:
                    print('{0},"{1}"'.format(row[0],row[1]))


main()
