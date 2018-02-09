
from random import randint, uniform
def gen_data(myfunc,n):
    R=[]
    for i in range(n):
        RR=[]
        t = i+uniform(-0.2,0.2)
        RR.append(t)
        RR.append(myfunc(t)*uniform(0.8,1.2))
        R.append(RR)
    return R

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(D,deg=1,objective=0):
  s,n = newSolver('Polynomial fitting'),len(D)
  b = s.infinity()
  a = [s.NumVar(-b,b,'a[%i]' % i) for i in range(1+deg)]  
  u = [s.NumVar(0,b,'u[%i]' % i) for i in range(n)]       
  v = [s.NumVar(0,b,'v[%i]' % i) for i in range(n)]       
  e = s.NumVar(0,b,'e')                                 
  for i in range(n):                              
    s.Add(D[i][1]==u[i]-v[i]+sum(a[j]*D[i][0]**j \
                                 for j in range(1+deg)))
  for i in range(n):                                     
    s.Add(u[i] <= e)
    s.Add(v[i] <= e)
  if objective:
    Cost = e                                               
  else:
    Cost = sum(u[i]+v[i] for i in range(n))                
  s.Minimize(Cost)
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(a)
