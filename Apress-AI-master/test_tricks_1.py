
from ortools.linear_solver import pywraplp  
from my_or_tools import SolVal, ObjVal
from my_or_tools_c import bounds_on_box
def main():
    bounds = []
    s = pywraplp.Solver('',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    a = [1,2]
    x = [s.NumVar(3,5,'x[%i]' % i) for i in range(2)]
    b = 10
    bounds = bounds_on_box(a,x,b)
    print(bounds==[-1,5])
main()
