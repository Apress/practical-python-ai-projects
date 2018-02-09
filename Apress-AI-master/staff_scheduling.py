
from random import randint
def gen_section(n):
  R=[]
  section=0
  for c in range(n):
    for j in range(randint(1,4)):
      RR=[section,c,randint(1,20)]
      R.append(RR)
      section = section+1
  return R,section

from random import randint
def gen_instructor(m,n,p,pp):
  R=[]
  for i in range(m):
    RR=[i,[randint(1,2),randint(2,3)],[randint(0,1)*randint(-10,10) for _ in range(p)],\
        [randint(0,1)*randint(-10,10) for _ in range(n)],\
        [randint(0,1)*randint(-10,10) for _ in range(pp)]
      ]
    R.append(RR)
  return R

from random import randint
def gen_sets(n,ns):
  R=[]
  for i in range(ns):
    RR=[i,[j for j in range(n) if randint(0,1)]]
    R.append(RR)
  return R

from random import randint
def gen_pairs(pp,n):
  R=[]
  for i in range(pp):
      q=4
      c0=0
      RR=[]
      for j in range(q):
        c0 = randint(c0,int(3*n/q))
        c1 = randint(c0+1,n-1)
        if (c0,c1) not in RR:
            RR.append((c0,c1))
      RR.sort()
      R.append([i,RR])
  return R

from my_or_tools import SolVal,ObjVal,newSolver
from my_or_tools import k_out_of_n, reify

def solve_model(S,I,R,P):
  s = newSolver('Staff Scheduling',True)
  nbS,nbI,nbSets,nbPairs = len(S),len(I),len(R),len(P)
  nbC,nbT = S[-1][1]+1,1+max(e[2] for e in S)
  x=[[s.IntVar(0,1,'') for _ in range(nbS)] for _ in range(nbI)] 
  z=[[[s.IntVar(0,1,'') for _ in range(len(P[p][1]))] \
        for p in range(nbPairs)] for _ in range(nbI)]
  for j in range(nbS): 
    k_out_of_n(s,1,[x[i][j] for i in range(nbI)],'<=')
  for i in range(nbI): 
    s.Add(sum(x[i][j] for j in range(nbS)) >= I[i][1][0])    
    s.Add(sum(x[i][j] for j in range(nbS)) <= I[i][1][1])
    for t in range(nbT): 
      k_out_of_n(s,1,
          [x[i][j] for j in range(nbS) if S[j][2]==t],'<=')
  WC=sum(x[i][j] * I[i][2][c] for i in range(nbI) \
     for j in range(nbS) for c in range(nbC) if S[j][1] == c) 
  WR=sum(I[i][3][r] * sum(x[i][j] for j in R[r][1]) \
     for r in range(nbSets) for i in range(nbI)) 
  for i in range(nbI): 
    for p in range(nbPairs):
      if I[i][4][p] != 0:
        for k in range(len(P[p][1])):
          xip1k0,xip1k1=x[i][P[p][1][k][0]],x[i][P[p][1][k][1]]
          reify(s,[1,1],[xip1k0,xip1k1],2,z[i][p][k],'>=')
  WP = sum(z[i][p][k]*I[i][4][p] for i in range(nbI) \
           for p in range(nbPairs) for k in range(len(P[p][1])) \
           if I[i][4][p] != 0) 
  s.Maximize(WC+WR+WP)
  rc,xs = s.Solve(),ss_ret(x,z,nbI,nbSets,nbS,nbPairs,I,S,R,P)
  return rc,SolVal(x),xs,ObjVal(s)

def ss_ret(x,z,nbI,nbSets,nbS,nbPairs,I,S,R,P):
    xs=[]
    for i in range(nbI):
      xs.append([i,[[j,(I[i][2][S[j][1]],\
         sum(I[i][3][r] for r in range(nbSets) if j in R[r][1]),
         sum(SolVal(z[i][p][k])*I[i][4][p]/2 
              for p in range(nbPairs) for k in range(len(P[p][1])) 
                if j in P[p][1][k]))] for j in range(nbS) \
                if SolVal(x[i][j])>0]])
    return xs
