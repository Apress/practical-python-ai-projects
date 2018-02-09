
from random import randint
from math import sqrt
def dist(p1,p2):
    return int(round(sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))/10)
def gen_data(n):
    points=[(randint(1,1000), randint(1,1000)) for i in range(n)]
    points.sort()
    R=[]
    S=0
    for i in range(n):
        RR=[]
        for j in range(n):
            if i==j or abs(i-j)>0.5*n:
                d = 0
            else:
                perturb = randint(0,1)
                d=None if perturb==0 else dist(points[i],points[j])*perturb
            RR.append(d)
        R.append(RR)
    return R

from my_or_tools import newSolver, SolVal, ObjVal

def solve_model(D,Start=None, End=None):
  s,n = newSolver('Shortest path problem'),len(D)
  if Start is None: 
    Start,End = 0,len(D)-1
  G = [[s.NumVar(0,1 if D[i][j] else 0,'') \
        for j in range(n)] for i in range(n)]
  for i in range(n): 
    if i == Start:
      s.Add(1 == sum(G[Start][j] for j in range(n))) 
      s.Add(0 == sum(G[j][Start] for j in range(n))) 
    elif i == End:
      s.Add(1 == sum(G[j][End] for j in range(n))) 
      s.Add(0 == sum(G[End][j] for j in range(n))) 
    else:
      s.Add(sum(G[i][j] for j in range(n)) ==
            sum(G[j][i] for j in range(n))) 
  s.Minimize(s.Sum(G[i][j]*(0 if D[i][j] is None else D[i][j]) \
                   for i in range(n) for j in range(n))) 
  rc = s.Solve()
  Path,Cost,Cumul,node=[Start],[0],[0],Start
  while rc == 0 and node != End and len(Path)<n:
    next = [i for i in range(n) if SolVal(G[node][i]) == 1][0]
    Path.append(next)
    Cost.append(D[node][next])
    Cumul.append(Cumul[-1]+Cost[-1])
    node = next
  return rc,ObjVal(s),Path,Cost,Cumul

def critical_tasks(D,t):
  s = set([t[i]+D[i][1] \
           for i in range(len(t))]+[t[i] for i in range(len(t))])
  n,ix,start,end,times = len(s),0,min(s),max(s),{}
  for e in s:
    times[e]=ix
    ix += 1
  M = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(len(t)): 
    M[times[t[i]]][times[t[i]+D[i][1]]] = -D[i][1]
  rc,v,Path,Cost,Cumul = solve_model(M,times[start],times[end])
  T = [i for i in range(len(t)) \
       for time in Path if times[t[i]+D[i][1]] == time]
  return rc, T

def solve_tree_model(D,Start=None):
  s,n = newSolver('Shortest paths tree problem'),len(D)
  Start = 0 if Start is None else Start 
  G = [[s.NumVar(0,0 if D[i][j] is None else min(n,D[i][j]),'')\
        for j in range(n)] for i in range(n)]
  for i in range(n):
    if i == Start:
      s.Add(n-1 == sum(G[Start][j] for j in range(n))) 
      s.Add(0 == sum(G[j][Start] for j in range(n))) 
    else:
      s.Add(sum(G[j][i] for j in range(n)) - \
            sum(G[i][j] for j in range(n))==1) 
  s.Minimize(s.Sum(G[i][j]*(0 if D[i][j] is None else D[i][j]) \
                   for i in range(n) for j in range(n))) 
  rc = s.Solve()
  Tree = [[i,j, D[i][j]] for i in range(n) for j in range(n) \
          if SolVal(G[i][j])>0]
  return rc,ObjVal(s),Tree

def solve_all_pairs(D):
  n = len(D)
  Costs =[[None if i != j else 0 for i in range(n)]\
    for j in range(n)]
  Paths =[[None for i in range(n)] for j in range(n)]
  for start in range(n):
    for end in range(n):
      if start != end and Costs[start][end] is None:
        rc, Value, Path, Cost, Cumul = solve_model(D,start,end)
        if rc==0:
          for k in range(len(Path)-1): 
            for l in range(k+1,len(Path)):
              if Costs[Path[k]][Path[l]] is None:
                Costs[Path[k]][Path[l]] = Cumul[l]-Cumul[k]
                Paths[Path[k]][Path[l]] = Path[k:l+1]
  return Paths, Costs
