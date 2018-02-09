
from random import randint,uniform,shuffle,sample
def gen_data(m,n):
    # m is number of jobs, n is the number of machines
    R=[]
    for j in range(m):
        p=list(range(n))
        p=sample(p,len(p))
        RR=[]
        for i in range(n):
            RR.append((p[i],randint(5,10)))
        R.append(RR)
    return R

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(D):
  s = newSolver('Job Shop Scheduling', True) 
  nJ,nM = len(D),len(D[0])
  M = sum([D[i][k][1] for i in range(nJ) for k in range(nM)]) 
  x = [[s.NumVar(0,M,'') for k in range(nM)] for i in range(nJ)]
  p = [[D[i][k][0] for k in range(nM)] for i in range(nJ)] 
  d = [[D[i][k][1] for k in range(nM)] for i in range(nJ)] 
  z = [[[s.IntVar(0,1,'') for k in range(nM)] \
        for j in range(nJ)] for i in range(nJ)]
  T = s.NumVar(0,M,'')
  for i in range(nJ):
    for k in range(nM):
      s.Add(x[i][p[i][k]] + d[i][k] <= T) 
      for j in range(nJ):
        if i != j: 
          s.Add(z[i][j][k] == 1-z[j][i][k])
          s.Add(x[i][p[i][k]] + d[i][k] - M*z[i][j][p[i][k]] \
                <= x[j][p[i][k]])
          s.Add(x[j][p[j][k]] + d[j][k] - M*z[j][i][p[j][k]] \
                <= x[i][p[j][k]])
    for k in range(nM-1):
      s.Add(x[i][p[i][k]] + d[i][k] <= x[i][p[i][k+1]]) 
  s.Minimize(T)
  rc = s.Solve()
  return rc,SolVal(T),SolVal(x)
