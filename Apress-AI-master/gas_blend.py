
from random import randint
def gen_raw(n):
    R=[]
    for i in range(n):
        R.append([randint(80,99),randint(600,1000),0])
    avgr=sum([R[i][0] for i in range(n)])/float(n)
    for i in range(n):
        p=randint(50,55)+4*R[i][0]/avgr
        R[i][2]=round(p,2)
    return R

from random import randint
def gen_refined(n):
      R=[]
      for i in range(n):
            R.append([randint(82,96),randint(100,500),randint(600,20000),0])
      avgr=sum([R[i][0] for i in range(n)])/float(n)
      for i in range(n):
            p=61.0+R[i][0]/avgr
            R[i][3]=round(p,2)
      return R

from my_or_tools import SolVal,ObjVal,newSolver

def solve_gas(C, D):
  s = newSolver('Gas blending problem')
  nR,nF = len(C),len(D)                                   
  Roc,Rmax,Rcost = 0,1,2
  Foc,Fmin,Fmax,Fprice = 0,1,2,3                             
  G = [[s.NumVar(0.0,10000,'') 
        for j in range(nF)] for i in range(nR)]
  R = [s.NumVar(0,C[i][Rmax],'') for i in range(nR)]
  F = [s.NumVar(D[j][Fmin],D[j][Fmax],'') for j in range(nF)]
  for i in range(nR):                                   
    s.Add(R[i] == sum(G[i][j] for j in range(nF)))
  for j in range(nF):
    s.Add(F[j] == sum(G[i][j] for i in range(nR)))
  for j in range(nF):                                     
    s.Add(F[j]*D[j][Foc] ==
          s.Sum([G[i][j]*C[i][Roc] for i in range(nR)]))
  Cost = s.Sum(R[i]*C[i][Rcost] for i in range(nR)) 
  Price = s.Sum(F[j]*D[j][Fprice] for j in range(nF))
  s.Maximize(Price - Cost)
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(G)
