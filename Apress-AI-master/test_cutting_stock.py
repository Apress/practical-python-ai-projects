
from cutting_stock import gen_data, solve_model, solve_large_model
import time
def main():
    import sys
    import random
    import tableutils
    n=7
    if len(sys.argv)<=1:
        print('Usage is main [data|run|large] [seed]')
        return
    elif len(sys.argv)>=3:
        random.seed(int(sys.argv[2]))
    C=gen_data(n)
    if sys.argv[1]=='data':
        tableutils.printmat(tableutils.wrapmat(C,[str(i) for i in range(n)],['Order','Nb rolls','% Width']))
    elif sys.argv[1]=='run':
        start = time.clock()
        rc,nb,rolls,w=solve_model(C)
        end = time.clock()
        if rc != 0:
            print('Infeasible')
        else:
            R = [[str(rolls[i][0]) , tableutils.set2string(tableutils.flatten(rolls[i][1:]))] for i in range(nb)]
            tableutils.printmat(tableutils.wrapmat(R,[str(i) for i in range(nb)],['rolls','Waste '+str(sum(w)),'Pattern']),True,0)
    elif sys.argv[1]=='large':
        #C = [[44, 81], [3,70],[48,68]]
        start = time.clock()
        rc,C,y,rolls=solve_large_model(C)  
        end = time.clock()
        nb = len(rolls)
        #tableutils.printmat(C)
        #tableutils.printmat([y])
        #tableutils.printmat(rolls)
        R = [[str(rolls[i][0]) , tableutils.set2string(tableutils.flatten(rolls[i][1:]))] for i in range(nb)]
        tableutils.printmat(tableutils.wrapmat(R,[str(i) for i in range(nb)],['rolls','Waste '+str(sum(rolls[i][0] for i in range(nb))),'Pattern ']),True,0)
main()
