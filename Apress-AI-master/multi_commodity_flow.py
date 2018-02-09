
from random import randint
import transship_dist
def gen_data(n,K):
  C=[transship_dist.gen_data(n,False) for _ in range(K)]
  X=[[0 for _ in range(n)] for _ in range(n)]
  for k in range(K):
    rc,Val,x = transship_dist.solve_model(C[k])
    if rc==0:
      for i in range(n):
        for j in range(n):
          X[i][j] += x[i][j]
  Cap = max([e for row in X for e in row])
  return C, Cap-100

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(C,D=None,Z=False):
  s = newSolver('Multi-commodity mincost flow problem', Z)
  K,n = len(C),len(C[0])-1,
  B = [sum(C[k][-1][j] for j in range(n)) for k in range(K)]
  x = [[[s.IntVar(0,B[k] if C[k][i][j] else 0,'') \
         if Z else s.NumVar(0,B[k] if C[k][i][j] else 0,'') \
         for j in range(n)] for i in range(n)] for k in range(K)]  
  for k in range(K): 
    for i in range(n): 
      s.Add(C[k][i][-1] - C[k][-1][i] == 
            sum(x[k][i][j] for j in range(n)) - \
            sum(x[k][j][i] for j in range(n)))
  if D:
    for i in range(n):
      for j in range(n):
        s.Add(sum(x[k][i][j] for k in range(K)) <= \
              D if type(D) in [int,float] else D[i][j])
  Cost = s.Sum(C[k][i][j]*x[k][i][j] if C[k][i][j] else 0\
         for i in range(n) for j in range(n) for k in range(K)) 
  s.Minimize(Cost)
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(x)

from my_or_tools import ObjVal, SolVal

def solve_all_pairs(D,sources=None):
  n,C = len(D),[]
  if sources is None:
    sources = [i for i in range(n)]
  for node in sources:
    C0 = [[0 if n in [i,j] else D[i][j] for j in range(n+1) ] \
          for i in range(n+1)] 
    C0[node][-1] = n-1
    for j in range(n):
      if j!= node:
        C0[-1][j] = 1
    C.append(C0)
  rc,Val,x = solve_model(C)
  Paths = [[None for _ in range(n)] for _ in sources]
  Costs = [[0 for _ in range(n)] for _ in sources]
  if rc == 0:
    for source in sources:
      ix = sources.index(source)
      for target in range(n):
        if source != target:
          Path,Cost,node = [target],0,target
          while Path[0] != source and len(Path)<n:
            v = [j for j in range(n) if x[ix][j][node]>=0.1][0]
            Path.insert(0,v)
            Cost += D[v][node]
            node = v
          Paths[ix][target] = Path
          Costs[ix][target] = Cost
  return rc, Paths, Costs
