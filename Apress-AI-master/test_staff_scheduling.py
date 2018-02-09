
from staff_scheduling import gen_section, gen_instructor, gen_pairs, solve_model, gen_sets
from my_or_tools import newSolver, ObjVal, SolVal
def main():
    import sys
    import random
    import tableutils
    nbcourse=7
    nbsets=6
    nbinstructor=5
    nbpairs=2
    if len(sys.argv)<=1:
        print('Usage is main [section|sets|instructor|pairs|run] [seed]')
        return
    elif len(sys.argv)>=3:
        random.seed(int(sys.argv[2]))
    S,nbsection=gen_section(nbcourse)
    R=gen_sets(nbsection,nbsets)
    I=gen_instructor(nbinstructor,nbsets,nbcourse,nbpairs)
    P=gen_pairs(nbpairs,nbsection)
    if sys.argv[1]=='section':
        tableutils.printmat(tableutils.wrapmat(S,[],['Id','Course id','Meeting Time']),True,0)
    elif sys.argv[1]=='sets':
        RR=[]
        for i in range(len(R)):
            RR.append([R[i][0],tableutils.set2string(R[i][1])])
        tableutils.printmat(tableutils.wrapmat(RR,[],['Id','Sections']),True,0)
    elif sys.argv[1]=='instructor':
        RI=[]
        for i in range(len(I)):
            RI.append([I[i][0],
                       tableutils.set2string(I[i][1]),
                       tableutils.set2string(I[i][2]),
                       tableutils.set2string(I[i][3]),
                       tableutils.set2string(I[i][4])])
        tableutils.printmat(tableutils.wrapmat(RI,[],['Id','Load','Course weights','Set weights','Pair weights']),True,0)
    elif sys.argv[1]=='pairs':
        RP=[]
        for i in range(len(P)):
            X=[str('(')+str(e[0])+str(' ')+str(e[1])+str(')') for e in P[i][1]]
            RP.append([P[i][0],tableutils.set2string(X)])
        tableutils.printmat(tableutils.wrapmat(RP,[],['Id','Section pairs']),True,0)
    elif sys.argv[1]=='run':
        rc,x,xs,v=solve_model(S,I,R,P)
        #tableutils.printmat(x)
        #print(xs)
        XS=[]
        for i in range(len(xs)):
            XS.append([xs[i][0], 
                       ['{0:2}'.format(e[0])+' : ('+'{0:2}'.format(e[1][0])+' '+'{0:2}'.format(e[1][1])+' '+'{0:2}'.format(e[1][2])+')' for e in xs[i][1]]])
        tableutils.printmat(tableutils.wrapmat(XS,[],['Instructor','Section (WC WR WP)']),True,1)
main()
