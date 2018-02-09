
from my_or_tools import SolVal, ObjVal, newSolver
from my_or_tools_c import bounds_on_box, reify_force
def main():
    s = newSolver('Test reify force',True)
    x = [s.NumVar(0,10,''),s.NumVar(0,10,'')]
    delta_1 = reify_force(s,[1,1],x,3,None,'==')
    delta_2 = reify_force(s,[1,1],x,5,None,'==')
    s.Add(delta_1+delta_2 == 1)
    s.Maximize(2*x[0] + 3*x[1])
    s.Solve()
    print([SolVal(delta_1)==0,SolVal(delta_2)==1,abs(SolVal(x[0]))<0.0001,abs(SolVal(x[1])-5)<0.0001])
    s = newSolver('Test reify force',True)
    x = [s.NumVar(0,10,''),s.NumVar(0,10,'')]
    delta_1 = reify_force(s,[1,1],x,3,None,'==')
    delta_2 = reify_force(s,[1,1],x,5,None,'==')
    s.Add(delta_1+delta_2 == 1)
    s.Minimize(2*x[0] + 3*x[1])
    s.Solve()
    print([SolVal(delta_1)==1,SolVal(delta_2)==0,abs(SolVal(x[0])-3)<0.0001,abs(SolVal(x[1]))<0.0001])
main()
