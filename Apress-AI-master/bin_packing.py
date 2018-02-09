
from random import randint,uniform
from math import ceil
def gen_data(n):
  R,T=[],0
  for i in range(n):
    RR=[randint(6,10),randint(200,500)]
    T+=RR[0]*RR[1]
    R.append(RR)
  return R,randint(1200, 1500)

from my_or_tools import newSolver, ObjVal, SolVal

def solve_model(D,W,symmetry_break=False,knapsack=True):
  s = newSolver('Bin Packing',True)
  nbC,nbP = len(D),sum([P[0] for P in D]) 
  w = [e for sub in [[d[1]]*d[0] for d in D] for e in sub] 
  nbT,nbTmin = bound_trucks(w,W)
  x = [[[s.IntVar(0,1,'')  for _ in range(nbT)] \
      for _ in range(d[0])] for d in D]
  y = [s.IntVar(0,1,'')  for _ in range(nbT)]
  for k in range(nbT): 
    sxk = sum(D[i][1]*x[i][j][k] \
              for i in range(nbC) for j in range(D[i][0]))
    s.Add(sxk <= W*y[k])  
  for i in range(nbC):
    for j in range(D[i][0]):
      s.Add(sum([x[i][j][k] for k in range(nbT)]) == 1)   
  if symmetry_break: 
    for k in range(nbT-1): 
      s.Add(y[k] >= y[k+1])
    for i in range(nbC):
      for j in range(D[i][0]):
        for k in range(nbT):
          for jj in range(max(0,j-1),j):
            s.Add(sum(x[i][jj][kk] \
              for kk in range(k+1)) >= x[i][j][k]) 
          for jj in range(j+1,min(j+2,D[i][0])):
            s.Add(sum(x[i][jj][kk] \
              for kk in range(k,nbT))>=x[i][j][k]) 
  if knapsack:
    s.Add(sum(W*y[i] for i in range(nbT)) >= sum(w))
  s.Add(sum(y[k] for k in range(nbT)) >= nbTmin)
  s.Minimize(sum(y[k] for k in range(nbT))) 
  rc = s.Solve()
  P2T=[[D[i][1], [k  for j in range(D[i][0]) for k in range(nbT)
                  if SolVal(x[i][j][k])>0]] for i in range(nbC) ]
  T2P=[[k, [(i,j,D[i][1]) \
    for i in range(nbC) for j in range(D[i][0])\
            if SolVal(x[i][j][k])>0]] for k in range(nbT)]
  return rc,ObjVal(s),P2T,T2P

def bound_trucks(w,W):
  nb,tot = 1,0
  for i in range(len(w)):
    if tot+w[i] < W:
      tot += w[i]
    else:
      tot = w[i]
      nb = nb+1
  return nb,ceil(sum(w)/W)
