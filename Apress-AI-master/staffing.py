
from random import randint, uniform
def gen_data(m,n,n0):
  # m is number of time intervals, n is number of shifts
  R = [[0 for _ in range(n+1)] for _ in range(m+1)]
  for i in range(m):            # Staffing needs
    R[i][-1] = randint(10,20)
  n1 = n-n0                     # Part-time
  d0 = int(round(m/n0)+1)       # Full-time shift
  d1 = int(round(d0/2))          # Part-time shift
  for j in range(n0):           # Pay for full-time-shift
    R[-1][j] = round(uniform(15,20)*d0,2)
  for j in range(n0,n):
    R[-1][j] = round(uniform(10,15)*d1,2)
  s = 0
  for j in range(n0):           # Full-time shift layout
    for i in range(s,s+d0):
      R[i%m][j] = 1
    s = s+d0-1
  s = [R[i][-1] for i in range(m)].index(max(R[i][-1] for i in range(m)))
  for j in range(n0,n):         # Part-time shift layout
    for i in range(s,s+d1):
      R[i%m][j] = 1
    s = s+d1+1
  return R

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(M,nf,Q=None,P=None,no_part=False):
  s = newSolver('Staffing', True)
  nbt,n = len(M)-1,len(M[0])-1
  B = sum(M[t][-1] for t in range(len(M)-1)) 
  x = [s.IntVar(0,B,'') for i in range(n)]
  for t in range(nbt): 
    s.Add(sum([M[t][i] * x[i] for i in range(n)])  >= M[t][-1]) 
  if Q:
    for i in range(n):
      s.Add(x[i] >= Q[i])
  if P:
    s.Add(sum(x[i] for i in range(nf)) >= P)
  if no_part:
    for t in range(nbt):
      s.Add(B*sum([M[t][i] * x[i] for i in range(nf)]) \
            >= sum([M[t][i] * x[i] for i in range(nf,n)]))
  s.Minimize(sum(x[i]*M[-1][i] for i in range(n)))
  rc = s.Solve()
  return rc, ObjVal(s), SolVal(x)
