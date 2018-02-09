
from my_or_tools import SolVal, newSolver
from my_or_tools_c import sosn

def minimize_piecewise_linear(Points,B,convex=True):
    s,n = newSolver('Piecewise', True),len(Points)
    x = s.NumVar(Points[0][0],Points[n-1][0],'x')
    l = [s.NumVar(0,1,'l[%i]' % (i,)) for i in range(n)]  
    s.Add(1 == sum(l[i] for i in range(n)))               
    d = sosn(s, 2, l)
    s.Add(x == sum(l[i]*Points[i][0] for i in range(n)))  
    s.Add(x >= B)                                                 
    Cost = s.Sum(l[i]*Points[i][1] for i in range(n))     
    s.Minimize(Cost)
    rc = s.Solve()
    return rc,SolVal(l),SolVal(d[1])
