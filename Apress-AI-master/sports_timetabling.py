
from random import randint, choice
def compute_weeks(T,P):
  from math import ceil
  nbTeams = sum([1 for sub in T for e in sub])
  nbIntra = P[0]
  nbInter = P[1]
  nbPerWeek = P[2]
  nbGames = 0
  nbWeeks = 0
  d = 1000
  for i in range(len(T)):
    nb = len(T[i])
    d = min(d,nb)
    nbGames += nb*(nb-1)/2 * nbIntra 
    for j in range(i+1,len(T)):
      nbGames += nb * len(T[j]) * nbInter
  nbWeeks = nbGames//d//nbPerWeek
  return int(nbWeeks)
def gen_data(m,n):
  R,team=[],0
  for i in range(m):
    RR=[]
    nb = choice(n)
    for j in range(nb):
      RR.append(team)
      team = team+1
    R.append(RR)
  X=randint(1,3)
  Y=randint(1,X)
  feasible = False
  Z=randint(1,5)
  while not feasible:
    Q=compute_weeks(R,(X,Y,Z))
    if Q<30:
      feasible=True
    else:
      Z=Z+1
  return R,(X,Y,Z,Q)

from my_or_tools import ObjVal, SolVal, newSolver, pairs

def solve_model(Teams,params):
  (nbIntra,nbInter,nbPerWeek,nbWeeks) = params
  nbTeams = sum([1 for sub in Teams for e in sub])
  nbDiv,Cal = len(Teams),[]
  s = newSolver('Sports schedule', True)
  x = [[[s.IntVar(0,1,'') if i<j else None
        for _ in range(nbWeeks)]  
        for j in range(nbTeams)] for i in range(nbTeams-1)]
  for Div in Teams: 
    for i in Div:
      for j in Div:
        if i<j:
          s.Add(sum(x[i][j][w] for w in range(nbWeeks))==nbIntra)
  for d in range(nbDiv-1): 
    for e in range(d+1,nbDiv):
      for i in Teams[d]:
        for j in Teams[e]:
          s.Add(sum(x[i][j][w] for w in range(nbWeeks))==nbInter)
  for w in range(nbWeeks):
    for i in range(nbTeams):
      s.Add(sum(x[i][j][w] for j in range(nbTeams) if i<j) + 
            sum(x[j][i][w] for j in range(nbTeams) if j<i )\
            <=nbPerWeek)
  Value=[x[i][j][w] for Div in Teams for i in Div for j in Div \
      for w in range(nbWeeks-len(Div)*nbIntra//nbPerWeek,nbWeeks)\
      if i<j]
  s.Maximize(sum(Value))
  rc = s.Solve()
  if rc == 0:
    Cal=[[(i,j) \
          for i in range(nbTeams-1) for j in range(i+1,nbTeams)\
          if SolVal(x[i][j][w])>0] for w in range(nbWeeks)]
  return rc,ObjVal(s),Cal

def add_intra(s,Teams,nbWeeks,nbIntra,x):
  for Div in Teams: 
    for i in Div:
      for j in Div:
        if i<j:
          s.Add(sum(x[i][j][w] for w in range(nbWeeks)) == nbIntra)

def add_inter(s,Teams,nbDiv,nbWeeks,nbInter,x):
  for d in range(nbDiv-1):
    for e in range(d+1,nbDiv):
      for i in Teams[d]:
        for j in Teams[e]:
          s.Add(sum(x[i][j][w] for w in range(nbWeeks)) == nbInter)

def add_games_bound(s,nbWeeks,nbTeams,nbPerWeek,x):
  for w in range(nbWeeks):
    for i in range(nbTeams):
      s.Add(sum(x[i][j][w] for j in range(nbTeams) if i<j) + 
            sum(x[j][i][w] for j in range(nbTeams) if j<i ) <= nbPerWeek)

def add_objective(s,Teams,nbWeeks,x,nbIntra,nbPerWeek):
  Value=[x[i][j][w] for Div in Teams for i in Div for j in Div \
         for w in range(nbWeeks-len(Div)*nbIntra//nbPerWeek,nbWeeks) if i<j]
  return Value

def basic_model(s,Teams,nbTeams,nbWeeks,nbPerWeek,nbIntra,nbDiv,nbInter,cuts,x):
    add_intra(s,Teams,nbWeeks,nbIntra,x)
    add_inter(s,Teams,nbDiv,nbWeeks,nbInter,x)
    add_games_bound(s,nbWeeks,nbTeams,nbPerWeek,x)  

    for t,w in cuts:
      s.Add(sum(x[p[0]][p[1]][w[0]] for p in pairs(t,[])) <= w[1])

    Value = add_objective(s,Teams,nbWeeks,x,nbIntra,nbPerWeek)
    s.Maximize(s.Sum(Value))

def solve_model_big(Teams,params):
  (nbIntra,nbInter,nbPerWeek,nbWeeks) = params
  nbTeams = sum([1 for sub in Teams for e in sub])
  nbDiv,cuts = len(Teams),[]
  for iter in range(2): 
    s = newSolver('Sports schedule', False)
    x = [[[s.NumVar(0,1,'') if i<j else None
          for _ in range(nbWeeks)] 
          for j in range(nbTeams)] for i in range(nbTeams-1)]
    basic_model(s,Teams,nbTeams,nbWeeks,nbPerWeek,nbIntra,\
                nbDiv,nbInter,cuts,x) 
    rc = s.Solve()
    bounds = {(3,1):1, (4,1):2, (5,1):2, (5,3):7}
    if nbPerWeek <= 3:
      for w in range(nbWeeks):
        for i in range(nbTeams-2):
          for j in range(i+1,nbTeams-1):
            for k in range(j+1,nbTeams):
              b = bounds.get((3,nbPerWeek),1000)
              if sum([SolVal(x[p[0]][p[1]][w]) \
                      for p in pairs([i,j,k],[])])>b:
                cuts.append([[i,j,k],[w,b]])
                for l in range(k+1,nbTeams):
                  b = bounds.get((4,nbPerWeek),1000)
                  if sum([SolVal(x[p[0]][p[1]][w]) \
                          for p in pairs([i,j,k,l],[])])>b:                  
                    cuts.append([[i,j,k,l],[w,b]])
                  for m in range(l+1, nbTeams):
                    b = bounds.get((5,nbPerWeek),1000)                    
                    if sum([SolVal(x[p[0]][p[1]][w]) \
                            for p in pairs([i,j,k,l,m],[])])>b:
                      cuts.append([[i,j,k,l,m],[w,b]])
    else:
      break
  s = newSolver('Sports schedule', True) 
  x = [[[s.IntVar(0,1,'') if i<j else None 
        for _ in range(nbWeeks)]
        for j in range(nbTeams)] for i in range(nbTeams-1)]
  basic_model(s,Teams,nbTeams,nbWeeks,nbPerWeek,nbIntra,\
              nbDiv,nbInter,cuts,x)
  rc,Cal = s.Solve(),[]
  if rc == 0:
    Cal=[[(i,j) \
          for i in range(nbTeams-1) for j in range(i+1,nbTeams)\
          if SolVal(x[i][j][w])>0] for w in range(nbWeeks)]
  return rc,ObjVal(s),Cal
