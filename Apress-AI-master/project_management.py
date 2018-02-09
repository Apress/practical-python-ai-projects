
from random import randint
def gen_data(n):
    R=[]
    S=0
    for i in range(n):
        RR=[i]                  # Task number
        RR.append(randint(2,8)) # Duration
        P=[]
        for j in range(i):
            if randint(0,1)*randint(0,1):
                P.append(j)
        RR.append(P) 
        R.append(RR)
    return R

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(D):
  s = newSolver('Project management')
  n = len(D)
  max = sum(D[i][1] for i in range(n))                           
  t = [s.NumVar(0,max,'t[%i]' % i) for i in range(n)]           
  Total = s.NumVar(0,max,'Total')                          
  for i in range(n):  
    s.Add(t[i]+D[i][1] <= Total)                   
    for j in D[i][2]:
      s.Add(t[j]+D[j][1] <= t[i])               
  s.Minimize(Total)
  rc = s.Solve()
  return rc, SolVal(Total),SolVal(t)

from my_or_tools import ObjVal, SolVal
from ortools.linear_solver import pywraplp
def solve_model_clp(D):
  t = 'Project management'
  s = pywraplp.Solver(t,pywraplp.Solver.CLP_LINEAR_PROGRAMMING)
  n = len(D)
  max = sum(D[i][1] for i in range(n))                           
  t = [s.NumVar(0,max,'t[%i]' % i) for i in range(n)]           
  Total = s.NumVar(0,max,'Total')                          
  for i in range(n):  
    s.Add(t[i]+D[i][1] <= Total)                   
    for j in D[i][2]:
      s.Add(t[j]+D[j][1] <= t[i])               
  s.Minimize(Total)
  rc = s.Solve()
  return rc, SolVal(Total),SolVal(t)
