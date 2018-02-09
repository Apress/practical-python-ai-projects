
from random import randint
def gen_data(m,n):
    R=[]
    S=0
    for i in range(m):
        RR=[]
        for j in range(n):
            yesno = 1-randint(0,1)*randint(0,1)
            RR.append(randint(10,30)*yesno)
        RR.append(randint(500,700))
        R.append(RR)
        S += RR[-1]            
    A = S/n                    
    RR = []
    for i in range(n):
        RR.append(randint(int(0.75*A), int(1.1*A)))
    RR.append(0)
    R.append(RR)
    return R

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(D):
  s = newSolver('Mincost flow problem')
  m,n = len(D)-1,len(D[0])-1
  B = sum([D[-1][j] for j in range(n)])
  G = [[s.NumVar(0,B if D[i][j] else 0,'') for j in range(n)] \
       for i in range(m)]  
  for i in range(m): 
    s.Add(D[i][-1] >= sum(G[i][j] for j in range(n))) 
  for j in range(n):
    s.Add(D[-1][j] == sum(G[i][j] for i in range(m))) 
  Cost=s.Sum(G[i][j]*D[i][j] for i in range(m)for j in range(n)) 
  s.Minimize(Cost)
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(G)
