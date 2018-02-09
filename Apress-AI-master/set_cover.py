
from random import randint,uniform
def gen_data(m,n):
    # m is number of subsets, n is the size of universe
    All=[0 for i in range(n)]
    while sum(All)<n:
        R=[]
        All=[0 for i in range(n)]
        p=0.8
        for i in range(m):
            RR=[]
            for j in range(n):
                if uniform(0,1) > p:
                    RR.append(j)
                    All[j]=1
            R.append(RR)
    return R,[randint(1,10) for i in range(m)]

from my_or_tools import ObjVal, SolVal
from ortools.linear_solver import pywraplp

def solve_model(D,C=None):
  t = 'Set Cover'
  s = pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
  s = pywraplp.Solver(t,s) 
  nbSup = len(D)
  nbParts = max([e for d in D for e in d])+1
  S = [s.IntVar(0,1,'')  for i in range(nbSup)] 
  for j in range(nbParts):
    s.Add(1 <= sum(S[i] for i in range(nbSup) if j in D[i])) 
  s.Minimize(s.Sum(S[i]*(1 if C is None else C[i]) \
    for i in range(nbSup))) 
  rc = s.Solve()
  Suppliers = [i for i in range(nbSup) if SolVal(S[i])>0]
  Parts = [[i for i in range(nbSup) \
    if j in D[i] and SolVal(S[i])>0] for j in range(nbParts)]
  return rc,ObjVal(s),Suppliers,Parts
