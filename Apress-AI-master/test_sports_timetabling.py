
from sports_timetabling import gen_data, solve_model, solve_model_big
import sys
sys.setrecursionlimit(10000)
def main():
    import sys
    import random
    import tableutils
    nbdiv=2
    nbteam=[6,7,8]
    if len(sys.argv)<=1:
        print('Usage is main [data|run|big] [seed]')
        return
    elif len(sys.argv)>=3:
        random.seed(int(sys.argv[2]))
    D,T=gen_data(nbdiv,nbteam)
    if sys.argv[1]=='data':
        R=[['(Intra Inter G/W Weeks)',tableutils.set2string(T)]]
        for i in range(len(D)):
            R.append(['Division '+str(i)+' teams',tableutils.set2string(D[i])])
        tableutils.printmat(R)
    elif sys.argv[1] in ['run','big','bug']:
        if sys.argv[1]=='big':
            D,T=gen_data(4,[6])
            T=(3,2,1,52)
            R=[['(Intra Inter G/W Weeks)',tableutils.set2string(T)]]
            for i in range(len(D)):
                R.append(['Division '+str(i)+' teams',tableutils.set2string(D[i])])
            tableutils.printmat(R)
            rc,v,Cal=solve_model_big(D,T)
        elif sys.argv[1] == 'bug':
            D=[[0, 1, 2, 3, 4, 5],
               [6, 7, 8, 9, 10, 11, 12],
               [13, 14, 15, 16, 17, 18],
               [19, 20, 21, 22, 23, 24, 25, 26]]
            T=(3, 1, 2, 28)
            rc,v,Cal=solve_model_big(D,T)
        else:
            rc,v,Cal=solve_model(D,T)
        if rc != 0:
            print('Infeasible')
        else:
            R=[['Week', 'Matches']]
            nbWeeks=T[3]
            week = 0
            for matches in Cal:
                RR=[]
                for match in matches:
                    RR.append(str(match[0]) + ' vs ' + str(match[1]))
                RR.insert(0,week)
                R.append(RR)
                week+=1
            tableutils.printmat(R,True,0)
main()
