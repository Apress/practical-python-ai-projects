
from facility_location import gen_dcost, gen_fcost, solve_model
def main():
    import sys
    import random
    import tableutils
    m=10
    n=7
    if len(sys.argv)<=1:
        print('Usage is main [dcost|fcost|run] [seed]')
        return
    elif len(sys.argv)>=2:
        random.seed(int(sys.argv[2]))
    D=gen_dcost(m,n)
    F=gen_fcost(m)
    if sys.argv[1]=='dcost':
        for i in range(m):
            D[i].insert(0,'Plant '+str(i))
        D[-1].insert(0,'Demand')
        D.insert(0,['From/To']+['City'+str(i) for i in range(n)]+['Supply'])
        tableutils.printmat(D)
    elif sys.argv[1]=='fcost':
        F=[F]
        F.insert(0,['Plant']+[str(i) for i in range(m)])
        F[1].insert(0,'Cost')
        tableutils.printmat(F)
    elif sys.argv[1]=='run':
        rc,Value,x,y,Fcost,Dcost=solve_model(D,F)
        T=[]
        for i in range(m):
          if y[i]:
            T.append(['Plant '+str(i)]+x[i])
        T=tableutils.wrapmat(T,[],['']+['City '+str(j) for j in range(n)])
        tableutils.printmat(T)
        #print(T)


main()
