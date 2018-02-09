
from random import randint,uniform
from math import sqrt
def dist(p1,p2):
  return int(round(10*sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)))
def gen_data(n):
  points=[(randint(1,100), randint(1,100)) for i in range(n)]
  R=[[None for i in range(n)] for j in range(n)]
  for i in range(n):
    for j in range(n):
      perturb = uniform(0.8,1.2)
      if i != j and perturb>0:
        R[i][j]=int(dist(points[i],points[j]) * perturb)
  return R,points

from my_or_tools import ObjVal, SolVal, newSolver

def solve_model_eliminate(D,Subtours=[]):
  s,n = newSolver('TSP', True),len(D)
  x = [[s.IntVar(0,0 if D[i][j] is None else 1,'') \
        for j in range(n)] for i in range(n)] 
  for i in range(n):  
    s.Add(1 == sum(x[i][j] for j in range(n))) 
    s.Add(1 == sum(x[j][i] for j in range(n))) 
    s.Add(0 == x[i][i])
  for sub in Subtours:
    K = [x[sub[i]][sub[j]]+x[sub[j]][sub[i]]\
         for i in range(len(sub)-1) for j in range(i+1,len(sub))]
    s.Add(len(sub)-1 >= sum(K))
  s.Minimize(s.Sum(x[i][j]*(0 if D[i][j] is None else D[i][j]) \
                   for i in range(n) for j in range(n))) 
  rc = s.Solve()
  tours = extract_tours(SolVal(x),n) 
  return rc,ObjVal(s),tours

def extract_tours(R,n):
  node,tours,allnodes = 0,[[0]],[0]+[1]*(n-1)
  while sum(allnodes) > 0:
    next = [i for i in range(n) if R[node][i]==1][0]
    if next not in tours[-1]:
      tours[-1].append(next)
      node = next
    else:
      node = allnodes.index(1)
      tours.append([node])
    allnodes[node] = 0
  return tours

def solve_model(D):
  subtours,tours = [],[]
  while len(tours) != 1:
    rc,Value,tours=solve_model_eliminate(D,subtours)
    if rc == 0:
      subtours.extend(tours)
  return rc,Value,tours[0]

def solve_model_p(D):
  n,n1 = len(D),len(D)+1
  E = [[0 if n in (i,j) else D[i][j] \
    for j in range(n1)] for i in range(n1)]
  rc,Value,tour = solve_model(E)
  i = tour.index(n)
  path = [tour[j] for j in range(i+1,n1)]+\
         [tour[j] for j in range(i)]
  return rc,Value,path

def solve_model_star(D):
  import shortest_path
  n = len(D)
  Paths, Costs = shortest_path.solve_all_pairs(D)
  rc,Value,tour = solve_model(Costs)
  Tour=[]
  for i in range(len(tour)):
    Tour.extend(Paths[tour[i]][tour[(i+1) % len(tour)]][0:-1])
  return rc,Value,Tour
