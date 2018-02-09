
from my_or_tools_c import k_out_of_n, sosn
from random import randint,seed
from my_or_tools import SolVal
from ortools.linear_solver import pywraplp  

import tableutils
def main():
  t = 'k out of n'
  n = 9
  seed(100)
  bound = [randint(5,15) for _ in range(n)]
  tableutils.printmat([['Max sum of']+bound])
  for k in range(1,n+1):
    s = pywraplp.Solver(t,pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x = [s.NumVar(0,bound[i],'') for i in range(n)]
    y = [s.NumVar(0,bound[i],'') for i in range(n)]
    Costx = sum(x[i] for i in range(n))
    Costy = sum(y[i] for i in range(n))
    s.Maximize(Costx+Costy)
    k_out_of_n(s,k,x,'==')
    ldg=sosn(s,k,y)
    rc = s.Solve()
    if rc != 0:
      print('Error', rc)
    sy = SolVal(y)
    sx = SolVal(x)
    yy = [[' ','x'][e>0] for e in sy]
    xx = [[' ','x'][e>0] for e in sx]

    tableutils.printmat(tableutils.wrapmat([xx,yy],
                                           ['{0}/{1}'.format(k,n),'Adjacent {0}/{1}'.format(k,n)],
                                           None),0,False)
  return rc

main()
