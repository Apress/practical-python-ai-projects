
from shortest_path import gen_data, solve_model, solve_all_pairs, solve_tree_model, critical_tasks
def main():
    import sys
    import random
    import tableutils
    n=13
    header = ['P'+str(i) for i in range(n)]
    if len(sys.argv)<=1:
        print('Usage is main [data|run|all|tree|pm] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    C=gen_data(n)
    if sys.argv[1]=='data':
        for i in range(n):
            C[i].insert(0,'P'+str(i))
        C.insert(0,['']+header)
        tableutils.printmat(C)
    elif sys.argv[1]=='run':
        rc,Value,Path,Cost,Cumul=solve_model(C)
        Path.insert(0,'Points')
        Cost.insert(0,'Distance')
        Cumul.insert(0,'Cumulative')
        T=[Path,Cost,Cumul]
        tableutils.printmat(T,True)
    elif sys.argv[1]=='all':
        Paths, Costs = solve_all_pairs(C)
        tableutils.printmat(tableutils.wrapmat(Costs,header,header))
    elif sys.argv[1]=='tree':
        rc, Val,Tree = solve_tree_model(C)
        if rc != 0:
            print('Infeasible')
        else: 
            tableutils.printmat(tableutils.wrapmat(Tree,[],['From','To','Distance']),True,0)
    elif sys.argv[1]=='pm':
        D=[[0,3],[1,6],[2,3],[3,2],[4,2],[5,7],[6,7],[7,5],[8,2],[9,7],[10,4],[11,5]]
        t=[0,3,0,3,9,0,9,16,21,21,21,3]
        rc,Path = critical_tasks(D,t)
        if rc != 0:
            print('Infeasible')
        else:
            print(Path)
main()
