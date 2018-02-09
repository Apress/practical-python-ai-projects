
from random import randint
def gen_data(n,zap=True):
    R,Cap=[],[]
    S,D=0,0
    for i in range(n):
        RR=[]
        for j in range(n):
            if zap:
                yesno=randint(0,1)
            else:
                yesno=1
            if i != j and (i<j or randint(0,1)*R[j][i]==0):
                RR.append(yesno*randint(10,30))
            else:
                RR.append(0)
        T = (0 if i == n-1 else randint(0,1)*randint(0,1))*randint(500,700)
        RR.append(T)
        R.append(RR)
        S += T
    A = S/n                    
    RR = []
    for i in range(n-1):
        if zap:
            yesno=1-(randint(0,1)*randint(0,1))
        else:
            yesno=1
        T = (1 if R[i][-1]==0 else 0)*yesno*randint(int(0.95*A), int(1.9*A))
        RR.append(T)
        D += T
    # Need to ensure balance
    T = S-D
    RR.append(T)
    D += T
    RR.append(0)
    R.append(RR)
    return R

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(D):
  s = newSolver('Transshipment problem')
  n = len(D[0])-1
  B = sum([D[-1][j] for j in range(n)])
  G = [[s.NumVar(0,B if D[i][j] else 0,'') \
      for j in range(n)] for i in range(n)]  
  for i in range(n): 
    s.Add(D[i][-1] - D[-1][i] ==  \
    sum(G[i][j] for j in range(n))-sum(G[j][i]for j in range(n)))
  Cost=s.Sum(G[i][j]*D[i][j] for i in range(n)for j in range(n)) 
  s.Minimize(Cost)
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(G)
