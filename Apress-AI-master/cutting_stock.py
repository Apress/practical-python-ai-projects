
from random import randint
def gen_data(n):
    R=[]
    S=0
    for i in range(n):
        R.append([randint(1,12), randint(5,40)])
    return R

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(D):
  s,n = newSolver('Cutting Stock', True), len(D)
  k,b  = bounds(D) 
  y = [s.IntVar(0,1,'') for i in range(k[1])] 
  x = [[s.IntVar(0,b[i],'') for j in range(k[1])] \
      for i in range(n)]
  w = [s.NumVar(0,100,'') for j in range(k[1])] 
  nb = s.IntVar(k[0],k[1],'')
  for i in range(n):  
    s.Add(sum(x[i][j] for j in range(k[1])) >= D[i][0]) 
  for j in range(k[1]):
    s.Add(sum(D[i][1]*x[i][j] for i in range(n)) <= 100*y[j]) 
    s.Add(100*y[j]-sum(D[i][1]*x[i][j] for i in range(n))==w[j]) 
    if j < k[1]-1: 
      s.Add(sum(x[i][j] for i in range(n)) >= \
            sum(x[i][j+1] for i in range(n)))
  Cost = s.Sum((j+1)*y[j] for j in range(k[1])) 
  s.Add(nb == s.Sum(y[j] for j in range(k[1])))
  s.Minimize(Cost)
  rc = s.Solve()
  rnb = SolVal(nb)
  return rc,rnb,rolls(rnb,SolVal(x),SolVal(w),D),SolVal(w)

def bounds(D):
  n, b, T, k, TT = len(D), [], 0, [0,1], 0
  for i in range(n):
    q,w = D[i][0], D[i][1]
    b.append(min(D[i][0],int(round(100/D[i][1]))))
    if T+q*w <= 100:
      T,TT = T+q*w,TT + q*w
    else:
      while q:
        if T+w <= 100:
          T,TT,q = T+w,TT+w, q-1
        else:
          k[1],T = k[1]+1, 0
  k[0] = int(round(TT/100+0.5))
  return k, b

def rolls(nb, x, w, D):
  R,n = [],len(x)
  for j in range(len(x[0])):
    RR=[abs(w[j])]+[int(x[i][j])*[D[i][1]] for i in range(n) \
                    if x[i][j]>0]
    R.append(RR)
  return R

from my_or_tools import ObjVal, SolVal, newSolver
from math import ceil

def solve_large_model(D):
  n,iter = len(D),0
  A = get_initial_patterns(D)
  while iter < 20: 
    rc,y,l = solve_master(A,[D[i][0] for i in range(n)])
    iter = iter + 1
    a,v = get_new_pattern(l,[D[i][1] for i in range(n)])
    for i in range(n):
      A[i].append(a[i])
  rc,y,l = solve_master(A,[D[i][0] for i in range(n)],True)  
  return rc,A,y,rolls_patterns(A, y, D)

def solve_master(C,b,integer=False):
  t = 'Cutting stock master problem'
  m,n,u = len(C),len(C[0]),[]
  s = newSolver(t,integer)
  y = [s.IntVar(0,1000,'') for j in range(n)] # right bound?
  Cost = sum(y[j] for j in range(n)) 
  s.Minimize(Cost)
  for i in range(m):
    u.append(s.Add(sum(C[i][j]*y[j] for j in range(n)) >= b[i])) 
  rc = s.Solve()
  y = [int(ceil(e.SolutionValue())) for e in y]
  return rc, y, [0 if integer else u[i].DualValue() \
                for i in range(m)]

def get_new_pattern(l,w):
  s = newSolver('Cutting stock slave', True)
  n = len(l)
  a = [s.IntVar(0,100,'') for i in range(n)]
  Cost = sum(l[i]*a[i] for i in range(n))
  s.Maximize(Cost)
  s.Add(sum(w[i]*a[i] for i in range(n)) <= 100) 
  rc = s.Solve()
  return SolVal(a), ObjVal(s)

def get_initial_patterns(D):
  n = len(D)
  return [[0 if j != i else 1 for j in range(n)]\
          for i in range(n)]

def rolls_patterns(C, y, D):
  R,m,n = [],len(C),len(y)
  for j in range(n):
    for _ in range(y[j]):
      RR=[]
      for i in range(m):
        if C[i][j]>0:
          RR.extend([D[i][1]]*int(C[i][j]))
      w=sum(RR)
      R.append([100-w,RR])
  return R
